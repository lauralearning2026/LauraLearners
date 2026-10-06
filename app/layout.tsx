import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = { title: "Laura Learning | Mathematics Teacher Support", description: "Open-source mathematics lesson support and professional learning for new and out-of-field teachers." };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
 return <html lang="en"><body><header className="nav"><a className="brand" href="/">LAURA<span>LEARNING</span></a><nav><a href="/portfolio">Portfolio</a><a href="/learn">Teacher support</a><a href="/impact">Impact</a><a href="mailto:Bkosgey6@gmail.com">Contact</a></nav></header>{children}<footer><strong>Laura Learning</strong><p>Mathematics teacher support designed from classroom experience.</p><small>© 2026 Brigid Kosgey · Apache 2.0</small></footer></body></html>;
}