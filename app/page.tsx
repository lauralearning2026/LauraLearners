const steps = [
  ["01", "Reflect", "Check your own reasoning with a short, private knowledge check on the mathematics behind each step.", "/learn/diagnostic", "Try the knowledge check"],
  ["02", "Understand", "Study a worked example with the reasoning spelled out, plus the misconceptions students most often bring.", "/learn/lesson", "See a worked example"],
  ["03", "Prepare", "Use a ready lesson outline and a 10–15 minute module to rehearse your explanation before class.", "/learn/lessons", "Browse resources"],
];

export default function Home() {
  return (
    <main>
      <section className="hero portfolioHero">
        <div className="heroCopy">
          <div className="eyebrow">OPEN TEACHER SUPPORT · SECONDARY MATHEMATICS</div>
          <h1>Support for every teacher <em>of mathematics.</em></h1>
          <p className="lead">Many math classes are taught by teachers working outside their original preparation. LauraLearning gives them free, classroom-grounded support (a quick knowledge check, worked explanations, and lesson resources), starting with Algebra I readiness.</p>
          <div className="actions">
            <a className="button" href="/learn/diagnostic">Try the knowledge check →</a>
            <a className="button secondary" href="/learn">Explore teacher support</a>
          </div>
          <p className="heroByline">Created by Brigid Kosgey, a mathematics teacher in Memphis, Tennessee.</p>
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

      <section className="portfolioOverview">
        <div className="eyebrow">HOW IT WORKS</div>
        <h2>Reflect. Understand. Prepare.</h2>
        <p>Each unit follows the same short path from checking your own understanding to walking into class ready to explain it.</p>
        <div className="homeSteps">
          {steps.map(([n, title, text, href, cta]) => (
            <a href={href} key={n}><span>{n}</span><strong>{title}</strong><p>{text}</p><small>{cta} →</small></a>
          ))}
        </div>
        <p className="statusNote"><strong>Early preview.</strong> One unit, linear equations, is available now. More units are in development. <a href="/learn/how-it-works">How the preview works</a></p>
      </section>

      <section className="portfolioOverview portfolioIntro">
        <div>
          <div className="eyebrow">ABOUT THE CREATOR</div>
          <h2>Built from the classroom.</h2>
          <p>LauraLearning grows out of daily work teaching Algebra II in a Memphis public high school, together with graduate study in instructional design and learning technology.</p>
          <a href="/about">About Brigid →</a>
        </div>
        <div>
          <div className="eyebrow">INSTRUCTIONAL DESIGN PORTFOLIO</div>
          <h2>Design work and coursework.</h2>
          <p>Projects, evaluation plans, and artifacts from my M.Ed. in Instructional Design and Educational Technology, alongside my design philosophy.</p>
          <a href="/portfolio">View the portfolio →</a>
        </div>
      </section>

      <section className="statement portfolioContact">
        <p>CONNECT</p>
        <h2>Interested in trying it with your teachers, or contributing?</h2>
        <a className="button" href="mailto:Bkosgey6@gmail.com">Get in touch →</a>
      </section>
    </main>
  );
}
