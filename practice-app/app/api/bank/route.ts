import { staffBank, studentBank } from "../../../lib/bank";
import { json, requireRole } from "../../../lib/http";

export const dynamic = "force-dynamic";

// Students get questions without answer keys; keys are checked on the server when they answer.
export async function GET(req: Request) {
  const u = await requireRole(req, ["student", "teacher", "admin"]);
  if (u instanceof Response) return u;
  return json(u.role === "student" ? studentBank() : staffBank());
}
