import type { Metadata } from "next";
import { categories } from "../lib/portfolio";

export const metadata: Metadata = { title: { absolute: "Brigid Kosgey | Instructional Design ePortfolio" } };

export default function Home() {
  return (
    <main>
      <section className="hero portfolioHero">
        <div className="heroCopy">
          <div className="eyebrow">INSTRUCTIONAL DESIGN · LEARNING TECHNOLOGY · MATHEMATICS EDUCATION</div>
          <h1>Brigid <em>Kosgey</em></h1>
          <p className="portfolioRole">Algebra II Teacher | Learning Designer</p>
          <p className="lead">Welcome to my professional ePortfolio. I design clear, practical learning experiences that connect what happens in the classroom with thoughtful assessment and educational technology.</p>
          <div className="actions">
            <a className="button" href="/portfolio">View my work →</a>
            <a className="button secondary" href="/resume">View my resume</a>
          </div>
        </div>
        <div className="heroArt" aria-hidden="true">
          <div className="heroOrange"></div><div className="heroGreen"></div>
          <div className="heroLeaf leafOne"></div><div className="heroLeaf leafTwo"></div><div className="heroLeaf leafThree"></div>
          <div className="heroDesk">
            <div className="heroLaptop"><div className="heroScreen"><span>y = x² − 4</span><svg viewBox="0 0 240 130"><path d="M15 65H225M120 10V120" stroke="#164536" strokeWidth="2"/><path d="M42 15Q120 212 198 15" fill="none" stroke="#ff5b00" strokeWidth="5"/></svg></div></div>
            <div className="heroBooks"><span>MATHEMATICS</span><span>TEACHING</span><span>LEARNING</span></div>
          </div>
        </div>
      </section>

      <section className="portfolioOverview portfolioIntro">
        <div>
          <div className="eyebrow">ABOUT ME</div>
          <h2>Teaching shapes my design.</h2>
          <p>I teach Algebra II at a public high school in Memphis, Tennessee, and I am completing an M.Ed. in Instructional Design and Educational Technology. My classroom is where I test what works: scaffolding, clear explanations, and feedback that points to the next step.</p>
          <a href="/about">Read more about me →</a>
        </div>
        <div>
          <div className="eyebrow">DESIGN PHILOSOPHY</div>
          <h2>Design for understanding.</h2>
          <p>Effective learning starts from prior knowledge, models the thinking behind each step, and releases responsibility gradually. My Learning Design Toolkit gathers the theories and models behind these choices.</p>
          <a href="/philosophy">Read my philosophy and toolkit →</a>
        </div>
      </section>

      <section className="portfolioOverview">
        <div className="eyebrow">PORTFOLIO</div>
        <h2>My work, by area of practice</h2>
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

      <section className="portfolioOverview homeResume">
        <div>
          <div className="eyebrow">RESUME</div>
          <h2>Experience and education</h2>
          <p>Algebra II teacher in Memphis, Tennessee · M.Ed. in Instructional Design and Educational Technology (in progress) · graduate coursework in Applied Artificial Intelligence · B.Ed. in Mathematics Education.</p>
        </div>
        <a className="button secondary" href="/resume">View my resume →</a>
      </section>

      <section className="statement portfolioContact">
        <p>CONTACT ME</p>
        <h2>Let's talk about learning design.</h2>
        <a className="button" href="/contact">Get in touch →</a>
      </section>

      <section className="portfolioOverview homeFeatured">
        <div className="eyebrow">FEATURED PROJECT · TEACHER SUPPORT</div>
        <h2>LauraLearning</h2>
        <p>An open-source project I designed and built: free, classroom-grounded support for teachers of mathematics, including those teaching outside their original preparation. It starts with a short knowledge check, worked explanations, and lesson resources for linear equations.</p>
        <div className="actions">
          <a className="button" href="/learn">Explore Teacher Support →</a>
          <a className="button secondary" href="/learn/diagnostic">Try the knowledge check</a>
        </div>
      </section>
    </main>
  );
}
