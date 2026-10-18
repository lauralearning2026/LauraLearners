import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://www.lauralearning.org"),
  title: { default: "LauraLearning | Mathematics Teacher Support", template: "%s | LauraLearning" },
  description: "Open, classroom-grounded support for teachers of mathematics, including those teaching outside their original preparation. Created by Brigid Kosgey.",
};

const links = [
  ["/learn", "Teacher Support"],
  ["/portfolio", "Portfolio"],
  ["/about", "About"],
  ["/philosophy", "Design Philosophy"],
];

function NavLinks() {
  return (
    <>
      {links.map(([href, label]) => (
        <a key={href} href={href}>{label}</a>
      ))}
      <a className="navContact" href="mailto:Bkosgey6@gmail.com">Contact</a>
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
            <nav aria-label="Main navigation"><a href="/">Home</a><NavLinks /></nav>
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
