import { createHash, timingSafeEqual } from "node:crypto";
import { q } from "../../../lib/db";
import { body, fail, json, serverError, text } from "../../../lib/http";
import { clearCookie, currentUser, formatCode, newCode, normalizeCode, sessionCookie } from "../../../lib/session";

export const dynamic = "force-dynamic";

async function teacherExists(): Promise<boolean> {
  const r = await q(`SELECT 1 FROM users WHERE role = 'teacher' LIMIT 1`);
  return r.length > 0;
}

export async function GET(req: Request) {
  try {
    const u = await currentUser(req);
    if (!u) return json({ signedIn: false, setupNeeded: !(await teacherExists()) });
    let className = "";
    if (u.class_id) {
      const c = await q(`SELECT name FROM classes WHERE id = $1::int`, [u.class_id]);
      className = c[0]?.name || "";
    }
    return json({ signedIn: true, role: u.role, label: u.label, className, code: u.role === "teacher" ? formatCode(u.code) : undefined });
  } catch (e) {
    return serverError(e);
  }
}

const same = (a: string, b: string) => {
  const x = createHash("sha256").update(a).digest(), y = createHash("sha256").update(b).digest();
  return timingSafeEqual(x, y);
};

export async function POST(req: Request) {
  const b = await body(req);
  try {
    if (b.action === "logout") return json({ ok: true }, 200, { "Set-Cookie": clearCookie() });

    if (b.action === "login") {
      const code = normalizeCode(b.code);
      const rows = code.length >= 6
        ? await q(`SELECT id, role FROM users WHERE code = $1::text AND active`, [code])
        : [];
      if (!rows.length) {
        await new Promise(r => setTimeout(r, 600));
        return fail("That code was not recognized. Check it with your teacher and try again.", 401);
      }
      return json({ ok: true, role: rows[0].role }, 200, { "Set-Cookie": sessionCookie(rows[0].id, req) });
    }

    if (b.action === "setup") {
      const key = process.env.SETUP_KEY || "";
      if (!key) return fail("Add a SETUP_KEY environment variable in Vercel, redeploy, then try again.", 400);
      if (!same(text(b.key, 200), key)) {
        await new Promise(r => setTimeout(r, 600));
        return fail("That setup key does not match.", 401);
      }
      let created: any[] = [];
      for (let i = 0; i < 5 && !created.length; i++) {
        created = await q(
          `INSERT INTO users (code, role, label)
           SELECT $1::text, 'teacher', 'Teacher'
           WHERE NOT EXISTS (SELECT 1 FROM users WHERE role = 'teacher')
           ON CONFLICT (code) DO NOTHING
           RETURNING id, code`,
          [newCode()],
        );
        if (!created.length && (await teacherExists())) return fail("This app is already set up. Sign in with your teacher code.", 409);
      }
      if (!created.length) return fail("Could not create a code. Try again.", 500);
      return json({ ok: true, code: formatCode(created[0].code) }, 200, { "Set-Cookie": sessionCookie(created[0].id, req) });
    }

    return fail("Unknown request.");
  } catch (e) {
    return serverError(e);
  }
}
