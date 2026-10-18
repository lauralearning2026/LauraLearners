import type { Metadata } from "next";

export const metadata: Metadata = { title: "Teacher Knowledge Check" };

export default function DiagnosticLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return children;
}
