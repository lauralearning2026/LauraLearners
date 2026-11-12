import { ITEMS } from "../../../lib/bank";
import { LOCAL_DAY, q } from "../../../lib/db";
import { json, requireRole, serverError } from "../../../lib/http";

export const dynamic = "force-dynamic";

// Class-level results only: administrators never receive student labels, codes or answers by student.
export async function GET(req: Request) {
  const u = await requireRole(req, ["admin", "teacher"]);
  if (u instanceof Response) return u;
  try {
    const classes = await q(
      `SELECT c.id, c.name, count(u.id)::int AS students
         FROM classes c LEFT JOIN users u ON u.class_id = c.id AND u.role = 'student' AND u.active
        GROUP BY c.id ORDER BY c.id`,
    );
    const rows = await q(
      `SELECT u.class_id, a.item_id, a.correct, a.user_id, ${LOCAL_DAY} AS day
         FROM answers a JOIN users u ON u.id = a.user_id
        WHERE u.role = 'student' AND u.class_id IS NOT NULL`,
    );
    const today = (await q(`SELECT to_char(now() AT TIME ZONE 'America/Chicago', 'YYYY-MM-DD') AS d`))[0].d as string;
    const weekStart = new Date(Date.parse(today + "T12:00:00Z") - 6 * 864e5).toISOString().slice(0, 10);
    const interventions = await q(`SELECT class_id, count(*)::int AS n FROM assignments GROUP BY class_id`);
    const out = classes.map(c => {
      const mine = rows.filter(r => r.class_id === c.id);
      const byCat: Record<string, [number, number]> = { SO: [0, 0], EI: [0, 0], FN: [0, 0], SP: [0, 0] };
      for (const r of mine) {
        const cat = ITEMS.get(r.item_id)?.category;
        if (cat && byCat[cat]) { byCat[cat][1]++; if (r.correct) byCat[cat][0]++; }
      }
      return {
        id: c.id, name: c.name, students: c.students, answers: mine.length,
        correct: mine.filter(r => r.correct).length,
        activeThisWeek: new Set(mine.filter(r => r.day >= weekStart).map(r => r.user_id)).size,
        byCategory: byCat,
        interventions: interventions.find(i => i.class_id === c.id)?.n || 0,
      };
    });
    return json({ classes: out, today });
  } catch (e) {
    return serverError(e);
  }
}
