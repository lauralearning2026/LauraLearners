import type { Metadata } from "next";
import { categories, projects } from "../../lib/portfolio";

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
