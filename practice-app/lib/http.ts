import { currentUser, type Role, type User } from "./session";

export function json(data: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...headers },
  });
}

export function fail(message: string, status = 400): Response {
  return json({ error: message }, status);
}

export async function body(req: Request): Promise<Record<string, any>> {
  try {
    const b = await req.json();
    return b && typeof b === "object" ? b : {};
  } catch {
    return {};
  }
}

/** Resolve the signed-in user and check their role, or return the error response to send. */
export async function requireRole(req: Request, roles: Role[]): Promise<User | Response> {
  try {
    const u = await currentUser(req);
    if (!u) return fail("Please sign in again.", 401);
    if (!roles.includes(u.role)) return fail("Your code does not have access to this page.", 403);
    return u;
  } catch (e) {
    return serverError(e);
  }
}

export function serverError(e: unknown): Response {
  console.error(e);
  const msg = e instanceof Error && /database/i.test(e.message) ? e.message : "Something went wrong on the server. Try again.";
  return fail(msg, 500);
}

export const int = (v: unknown): number | null => {
  if (v === null || v === undefined || v === "") return null;
  const n = Number(v);
  return Number.isInteger(n) ? n : null;
};

export const text = (v: unknown, max = 80): string => String(v ?? "").trim().slice(0, max);
