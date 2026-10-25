import type { Metadata } from "next";
import { categories, projects, roadmap } from "../../lib/portfolio";

export const metadata: Metadata = { title: "Instructional Design Portfolio" };

export default function Portfolio() {
  return (
    <main className="page portfolioPage">
      <div className="eyebrow">INSTRUCTIONAL DESIGN PORTFOLIO</div>
      <h1>Problems worth solving.<br /><em>Products worth using.</em></h1>
      <p className="lead">A growing collection of learning experiences, systems, and research-informed design work.</p>

      <section className="portfolioCategories">
        <div className="eyebrow">ACE EPORTFOLIO CATEGORIES</div>
        <h2>Browse by area of practice</h2>
        <p>Each area has its own page, where new artifacts will appear as I complete my M.Ed. coursework.</p>
        <div className="categoryBoxes">
          {categories.map((c, i) => (
            <a className="categoryBox" href={`/portfolio/${c.slug}`} key={c.slug}>
              <span className="categoryIcon" aria-hidden="true">{c.icon}</span>
              <span className="eyebrow">0{i + 1} / 05</span>
              <h3>{c.name}</h3>
              <p>{c.description}</p>
              <span className={c.artifacts.length ? "wipBadge started" : "wipBadge"}>
                {c.artifacts.length ? "Work in progress · more to come" : "Future work · coming with coursework"}
              </span>
              <small>Open {c.name} →</small>
            </a>
          ))}
        </div>
      </section>

      <section className="roadmap">
        <div className="eyebrow">PROGRAM ROADMAP</div>
        <h2>Building my ePortfolio, step by step</h2>
        <p>Each course in my M.Ed. in Instructional Design and Educational Technology adds artifacts to this portfolio, leading to a comprehensive ePortfolio at the capstone.</p>
        <ol className="roadmapList">
          {roadmap.map(r => (
            <li key={r.step} className={r.done ? "done" : ""}>
              <span className="roadmapStep" aria-hidden="true">{r.done ? "✓" : r.step}</span>
              <div>
                <small>{r.course}{r.done ? " · Complete" : " · Upcoming"}</small>
                <strong>{r.href ? <a href={r.href}>{r.artifacts}</a> : r.artifacts}</strong>
                <p>{r.purpose}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="portfolioExisting">
        <h2>Projects</h2>
        <div className="projects">
          {projects.map((p, i) => (
            <article key={p.title}>
              <span>0{i + 1}</span>
              <div><small>{p.tag}</small><h2>{p.title}</h2><p>{p.summary}</p>{p.href && <a className="projectLink" href={p.href}>View project →</a>}</div>
            </article>
          ))}
        </div>
      </section>

      <section className="portfolioProjectLink">
        <h2>Explore LauraLearning</h2>
        <p>See the working mathematics teacher-support project.</p>
        <a className="button" href="/learn">Visit LauraLearning →</a>
      </section>
    </main>
  );
}
