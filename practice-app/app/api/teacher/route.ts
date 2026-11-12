import { ITEMS, baseStandard } from "../../../lib/bank";
import { LOCAL_DAY, q } from "../../../lib/db";
import { body, fail, int, json, requireRole, serverError, text } from "../../../lib/http";
import { formatCode, newCode } from "../../../lib/session";

export const dynamic = "force-dynamic";

const DEFAULT_RULES = { minN: 8, minDays: 2, cut: 60, errN: 3 };
const RULE_LIMITS: Record<string, [number, number]> = { minN: [3, 30], minDays: [1, 10], cut: [20, 95], errN: [2, 10] };

async function rules() {
  const r = await q(`SELECT value FROM settings WHERE key = 'rules'`);
  return { ...DEFAULT_RULES, ...(r[0]?.value || {}) };
}

async function createCode(role: string, label: string, classId: number | null) {
  for (let i = 0; i < 8; i++) {
    const r = await q(
      `INSERT INTO users (code, role, label, class_id) VALUES ($1::text, $2::text, $3::text, $4::int)
       ON CONFLICT (code) DO NOTHING RETURNING id, code, label`,
      [newCode(), role, label, classId],
    );
    if (r.length) return r[0];
  }
  throw new Error("Could not create a unique code.");
}

export async function GET(req: Request) {
  const u = await requireRole(req, ["teacher"]);
  if (u instanceof Response) return u;
  try {
    const classes = await q(`SELECT id, name FROM classes ORDER BY id`);
    const url = new URL(req.url);
    const classId = int(url.searchParams.get("classId")) ?? classes[0]?.id ?? null;
    const users = await q(`SELECT id, role, label, class_id, code, active FROM users ORDER BY role, class_id NULLS FIRST, label, id`);
    const answers = classId == null ? [] : await q(
      `SELECT a.user_id, a.item_id, ${LOCAL_DAY} AS day, a.correct, a.err, a.assignment_id
         FROM answers a JOIN users s ON s.id = a.user_id
        WHERE s.role = 'student' AND s.class_id = $1::int
        ORDER BY a.id`,
      [classId],
    );
    const assignments = await q(
      `SELECT id, class_id, standard, item_ids, user_ids, note,
              to_char(created_at AT TIME ZONE 'America/Chicago', 'YYYY-MM-DD') AS day
         FROM assignments WHERE NOT closed ORDER BY id DESC`,
    );
    const progress = await q(
      `SELECT assignment_id, user_id, count(DISTINCT item_id)::int AS n,
              count(DISTINCT item_id) FILTER (WHERE correct)::int AS c
         FROM answers WHERE assignment_id IS NOT NULL GROUP BY assignment_id, user_id`,
    );
    const dismissed = await q(`SELECT class_id, standard FROM dismissed`);
    const today = (await q(`SELECT to_char(now() AT TIME ZONE 'America/Chicago', 'YYYY-MM-DD') AS d`))[0].d;
    return json({
      today,
      classId,
      rules: await rules(),
      classes: classes.map(c => ({ id: c.id, name: c.name })),
      users: users.map(x => ({ id: x.id, role: x.role, label: x.label, classId: x.class_id, code: formatCode(x.code), active: x.active, me: x.id === u.id })),
      answers: answers.map(a => [a.user_id, a.item_id, a.day, a.correct ? 1 : 0, a.err, a.assignment_id]),
      assignments: assignments.map(a => ({
        id: a.id, classId: a.class_id, standard: a.standard, itemIds: a.item_ids, userIds: a.user_ids, note: a.note, day: a.day,
        progress: Object.fromEntries(progress.filter(p => p.assignment_id === a.id).map(p => [p.user_id, [p.c, p.n]])),
      })),
      dismissed: dismissed.map(d => [d.class_id, d.standard]),
    });
  } catch (e) {
    return serverError(e);
  }
}

export async function POST(req: Request) {
  const u = await requireRole(req, ["teacher"]);
  if (u instanceof Response) return u;
  const b = await body(req);
  try {
    switch (b.action) {
      case "addClass": {
        const name = text(b.name, 60);
        if (!name) return fail("Give the class a name, such as Period 2.");
        const r = await q(`INSERT INTO classes (name) VALUES ($1::text) RETURNING id`, [name]);
        return json({ ok: true, id: r[0].id });
      }
      case "renameClass": {
        const name = text(b.name, 60);
        if (!name) return fail("Give the class a name.");
        await q(`UPDATE classes SET name = $2::text WHERE id = $1::int RETURNING id`, [int(b.classId), name]);
        return json({ ok: true });
      }
      case "makeCodes": {
        const classId = int(b.classId);
        const count = int(b.count) ?? 0;
        if (count < 1 || count > 60) return fail("Make between 1 and 60 codes at a time.");
        const cls = await q(`SELECT id, name FROM classes WHERE id = $1::int`, [classId]);
        if (!cls.length) return fail("Choose a class first.");
        const prefix = text(b.prefix, 20) || "Student ";
        const existing = await q(`SELECT label FROM users WHERE class_id = $1::int AND role = 'student'`, [classId]);
        let n = 0;
        for (const e of existing) {
          if (e.label.startsWith(prefix)) n = Math.max(n, Number(e.label.slice(prefix.length)) || 0);
        }
        const made = [];
        for (let i = 1; i <= count; i++) {
          made.push(await createCode("student", `${prefix}${String(n + i).padStart(2, "0")}`, classId));
        }
        return json({ ok: true, made: made.map(m => ({ label: m.label, code: formatCode(m.code) })) });
      }
      case "addAdmin": {
        const label = text(b.label, 60) || "Administrator";
        const m = await createCode("admin", label, null);
        return json({ ok: true, label: m.label, code: formatCode(m.code) });
      }
      case "newCode": {
        const r = await q(`SELECT id FROM users WHERE id = $1::int`, [int(b.userId)]);
        if (!r.length) return fail("That person was not found.");
        for (let i = 0; i < 8; i++) {
          const x = await q(`UPDATE users SET code = $2::text WHERE id = $1::int AND NOT EXISTS (SELECT 1 FROM users WHERE code = $2::text) RETURNING code`, [r[0].id, newCode()]);
          if (x.length) return json({ ok: true, code: formatCode(x[0].code) });
        }
        return fail("Could not create a new code. Try again.", 500);
      }
      case "setLabel": {
        const label = text(b.label, 60);
        if (!label) return fail("Labels cannot be empty.");
        await q(`UPDATE users SET label = $2::text WHERE id = $1::int AND role <> 'teacher' RETURNING id`, [int(b.userId), label]);
        return json({ ok: true });
      }
      case "setActive": {
        await q(`UPDATE users SET active = $2::boolean WHERE id = $1::int AND role <> 'teacher' RETURNING id`, [int(b.userId), !!b.active]);
        return json({ ok: true });
      }
      case "deleteUser": {
        const id = int(b.userId);
        const r = await q(`SELECT role FROM users WHERE id = $1::int`, [id]);
        if (!r.length || r[0].role === "teacher") return fail("That person cannot be deleted here.");
        await q(`UPDATE assignments SET user_ids = array_remove(user_ids, $1::int) WHERE $1::int = ANY(user_ids) RETURNING id`, [id]);
        await q(`DELETE FROM users WHERE id = $1::int RETURNING id`, [id]);
        return json({ ok: true });
      }
      case "deleteAllStudentData": {
        if (b.confirm !== "DELETE") return fail("Type DELETE to confirm.");
        await q(`DELETE FROM assignments RETURNING id`);
        await q(`DELETE FROM dismissed RETURNING class_id`);
        await q(`DELETE FROM users WHERE role = 'student' RETURNING id`);
        return json({ ok: true });
      }
      case "assign": {
        const classId = int(b.classId);
        const standard = text(b.standard, 40);
        const students = await q(`SELECT id FROM users WHERE class_id = $1::int AND role = 'student' AND active`, [classId]);
        const allowed = new Set(students.map(s => s.id));
        const userIds = (Array.isArray(b.userIds) ? b.userIds : []).map(Number).filter((n: number) => allowed.has(n));
        const itemIds = (Array.isArray(b.itemIds) ? b.itemIds : []).map(String)
          .filter((id: string) => ITEMS.has(id) && baseStandard(ITEMS.get(id)!.standard) === standard).slice(0, 30);
        if (!userIds.length || !itemIds.length) return fail("Choose at least one student and one question.");
        const r = await q(
          `INSERT INTO assignments (class_id, standard, item_ids, user_ids, note)
           VALUES ($1::int, $2::text, $3::text[], $4::int[], $5::text) RETURNING id`,
          [classId, standard, itemIds, userIds, text(b.note, 600)],
        );
        return json({ ok: true, id: r[0].id });
      }
      case "closeAssignment": {
        await q(`UPDATE assignments SET closed = true WHERE id = $1::int RETURNING id`, [int(b.id)]);
        return json({ ok: true });
      }
      case "dismiss": {
        await q(`INSERT INTO dismissed (class_id, standard) VALUES ($1::int, $2::text) ON CONFLICT DO NOTHING RETURNING class_id`, [int(b.classId), text(b.standard, 40)]);
        return json({ ok: true });
      }
      case "restoreDismissed": {
        await q(`DELETE FROM dismissed WHERE class_id = $1::int RETURNING class_id`, [int(b.classId)]);
        return json({ ok: true });
      }
      case "rules": {
        const next: Record<string, number> = { ...(await rules()) };
        for (const [k, [lo, hi]] of Object.entries(RULE_LIMITS)) {
          const v = int(b.rules?.[k]);
          if (v != null) next[k] = Math.max(lo, Math.min(hi, v));
        }
        await q(
          `INSERT INTO settings (key, value) VALUES ('rules', $1::jsonb)
           ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value RETURNING key`,
          [JSON.stringify(next)],
        );
        return json({ ok: true, rules: next });
      }
      default:
        return fail("Unknown request.");
    }
  } catch (e) {
    return serverError(e);
  }
}

