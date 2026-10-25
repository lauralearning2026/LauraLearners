import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { categories, projects } from "../../../lib/portfolio";

type Params = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return categories.map(c => ({ slug: c.slug }));
}

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { slug } = await params;
  const c = categories.find(x => x.slug === slug);
  return { title: c ? `${c.name} · Portfolio` : "Portfolio" };
}

export default async function CategoryPage({ params }: Params) {
  const { slug } = await params;
  const index = categories.findIndex(x => x.slug === slug);
  if (index < 0) notFound();
  const c = categories[index];
  const prev = categories[(index + categories.length - 1) % categories.length];
  const next = categories[(index + 1) % categories.length];

  return (
    <main className="page compactPage categoryPage">
      <a className="backLink" href="/portfolio">← Portfolio</a>
      <div className="eyebrow">PORTFOLIO · 0{index + 1} / 05</div>
      <h1>{c.name.split(" ").slice(0, -1).join(" ")} <em>{c.name.split(" ").slice(-1)}</em></h1>
      <p className="lead">{c.description}</p>

      <div className="wipBanner">
        <span aria-hidden="true">🚧</span>
        <div>
          <strong>{c.artifacts.length ? "Work in progress" : "Future work"}</strong>
          <p>{c.artifacts.length
            ? "This area already has work to show, and more artifacts will be added from upcoming M.Ed. courses."
            : "Artifacts for this area will be added as I complete upcoming courses in my M.Ed. in Instructional Design and Educational Technology."}</p>
        </div>
      </div>

      {c.artifacts.length > 0 && (
        <>
          <h2>Current work</h2>
          {c.artifacts.map(i => (
            <div className="portfolioArtifact" key={i}>
              <small className="artifactTag">{projects[i].tag}</small>
              <strong>{projects[i].title}</strong>
              <p>{projects[i].summary}</p>
              {projects[i].href && <a className="projectLink" href={projects[i].href}>View project →</a>}
            </div>
          ))}
        </>
      )}

      <h2>Coming soon</h2>
      <div className="placeholderGrid">
        {c.planned.map((p, i) => (
          <div className="placeholderCard" key={p}>
            <div className="placeholderArt" aria-hidden="true">
              <span>{c.icon}</span>
            </div>
            <small>ARTIFACT {String(i + 1).padStart(2, "0")}</small>
            <strong>{p}</strong>
            <p>Reserved for an upcoming assignment.</p>
          </div>
        ))}
      </div>

      <nav className="categoryPager" aria-label="Other portfolio areas">
        <a href={`/portfolio/${prev.slug}`}>← {prev.name}</a>
        <a href={`/portfolio/${next.slug}`}>{next.name} →</a>
      </nav>
    </main>
  );
}
