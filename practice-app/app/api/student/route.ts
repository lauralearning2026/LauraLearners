import { ITEMS, baseStandard, grade } from "../../../lib/bank";
import { LOCAL_DAY, q } from "../../../lib/db";
import { body, fail, int, json, requireRole, serverError } from "../../../lib/http";

export const dynamic = "force-dynamic";

export async function GET(req: Request) {
  const u = await requireRole(req, ["student"]);
  if (u instanceof Response) return u;
  try {
    const answers = await q(
      `SELECT item_id, ${LOCAL_DAY} AS day, correct FROM answers WHERE user_id = $1::int ORDER BY id`,
      [u.id],
    );
    const assignments = await q(
      `SELECT a.id, a.standard, a.item_ids, a.note,
              to_char(a.created_at AT TIME ZONE 'America/Chicago', 'YYYY-MM-DD') AS day,
              (SELECT count(DISTINCT x.item_id)::int FROM answers x WHERE x.assignment_id = a.id AND x.user_id = $1::int) AS answered,
              (SELECT count(DISTINCT x.item_id)::int FROM answers x WHERE x.assignment_id = a.id AND x.user_id = $1::int AND x.correct) AS right_count,
              (SELECT coalesce(array_agg(DISTINCT x.item_id), '{}'::text[]) FROM answers x WHERE x.assignment_id = a.id AND x.user_id = $1::int) AS answered_ids
         FROM assignments a
        WHERE NOT a.closed AND $1::int = ANY(a.user_ids)
        ORDER BY a.id DESC`,
      [u.id],
    );
    return json({
      answers: answers.map(a => [a.item_id, a.day, a.correct ? 1 : 0]),
      assignments: assignments.map(a => ({
        id: a.id, standard: a.standard, itemIds: a.item_ids, note: a.note, day: a.day,
        answered: a.answered, right: a.right_count, answeredIds: a.answered_ids,
      })),
    });
  } catch (e) {
    return serverError(e);
  }
}

export async function POST(req: Request) {
  const u = await requireRole(req, ["student"]);
  if (u instanceof Response) return u;
  const b = await body(req);
  if (b.action !== "answer") return fail("Unknown request.");
  const item = ITEMS.get(String(b.itemId));
  if (!item) return fail("That question no longer exists. Start a new set.");
  const picked = Array.isArray(b.pick) ? b.pick.map(Number) : [];
  if (!picked.length) return fail("Choose an answer first.");
  try {
    let assignmentId: number | null = null;
    if (b.assignmentId != null) {
      assignmentId = int(b.assignmentId);
      const a = await q(
        `SELECT id FROM assignments WHERE id = $1::int AND NOT closed AND $2::int = ANY(user_ids) AND $3::text = ANY(item_ids)`,
        [assignmentId, u.id, item.id],
      );
      if (!a.length) assignmentId = null;
    }
    const g = grade(item, picked);
    await q(
      `INSERT INTO answers (user_id, item_id, standard, correct, picked, err, assignment_id)
       VALUES ($1::int, $2::text, $3::text, $4::boolean, $5::int[], $6::text, $7::int) RETURNING id`,
      [u.id, item.id, baseStandard(item.standard), g.correct, g.pick, g.err, assignmentId],
    );
    return json({ correct: g.correct, answer: item.answer, rationales: item.rationales, explanation: item.explanation });
  } catch (e) {
    return serverError(e);
  }
}
