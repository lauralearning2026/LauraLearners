import type { Metadata } from "next";
import "./globals.css";
import { categories } from "../lib/portfolio";

export const metadata: Metadata = {
  metadataBase: new URL("https://www.lauralearning.org"),
  title: { default: "LauraLearning | Mathematics Teacher Support", template: "%s | LauraLearning" },
  description: "Open, classroom-grounded support for teachers of mathematics, including those teaching outside their original preparation. Created by Brigid Kosgey.",
};

const aceLinks = [
  ["/about", "About Me"],
  ["/philosophy", "Design Philosophy"],
];
const aceAfter = [
  ["/resume", "Resume"],
  ["/contact", "Contact Me"],
];

function NavLinks({ mobile = false }: { mobile?: boolean }) {
  return (
    <>
      {aceLinks.map(([href, label]) => <a key={href} href={href}>{label}</a>)}
      {mobile ? (
        <>
          <a href="/portfolio">Portfolio</a>
          {categories.map(c => <a key={c.slug} className="navSub" href={`/portfolio/${c.slug}`}>{c.name}</a>)}
        </>
      ) : (
        <div className="navDrop">
          <a href="/portfolio" aria-haspopup="true">Portfolio ▾</a>
          <div className="navDropMenu">
            {categories.map(c => <a key={c.slug} href={`/portfolio/${c.slug}`}>{c.name}</a>)}
          </div>
        </div>
      )}
      {aceAfter.map(([href, label]) => <a key={href} href={href}>{label}</a>)}
      <a className="navTeacher" href="/learn">Teacher Support</a>
    </>
  );
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,600&family=Public+Sans:wght@400;600;700;800&display=swap"
        />
      </head>
      <body>
        <header className="nav">
          <a className="brand" href="/">LAURA<span>LEARNING</span></a>
          <nav className="navDesktop" aria-label="Main navigation"><NavLinks /></nav>
          <details className="navMobile">
            <summary aria-label="Open menu"><span /><span /><span /></summary>
            <nav aria-label="Main navigation"><a href="/">Home</a><NavLinks mobile /></nav>
          </details>
        </header>
        {children}
        <footer>
          <strong>LauraLearning</strong>
          <p>Open mathematics teacher support, designed from classroom experience by Brigid Kosgey.</p>
          <small>© 2026 Brigid Kosgey · Source code licensed under Apache 2.0</small>
        </footer>
      </body>
    </html>
  );
}
