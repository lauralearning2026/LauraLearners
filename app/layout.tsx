import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = { title: "Laura Learning | Adaptive Learning & Instructional Design", description: "Open, classroom-grounded adaptive learning and authentic instructional design." };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
 return <html lang="en"><body><header className="nav"><a className="brand" href="/">LAURA<span>LEARNING</span></a><nav><a href="/portfolio">Portfolio</a><a href="/learn">LauraLearners</a><a href="/impact">Impact</a><a href="mailto:Bkosgey6@gmail.com">Contact</a></nav></header>{children}<footer><strong>Laura Learning</strong><p>Open learning technology designed from classroom experience.</p><small>© 2026 Brigid Kosgey · Apache 2.0</small></footer></body></html>;
}