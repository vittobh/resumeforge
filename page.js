(function () {
  const state = {
    resumeText: "",
    resumeName: "",
    jdText: "",
    parsedJD: null,
    questions: [],
    generated: null,
  };

  const skillTerms = [
    "agentic ai", "rag", "ai", "api", "roadmap", "prd", "brd", "analytics",
    "healthcare", "bfsi", "fhir", "hl7", "kyc", "aml", "snowflake", "saas",
    "stakeholder", "agile", "scrum", "data", "platform", "governance"
  ];

  function $(id) {
    return document.getElementById(id);
  }

  function banner(message, ok = false) {
    if (window.app?.banner) window.app.banner(message, ok);
  }

  function unique(list) {
    return [...new Set(list.filter(Boolean))];
  }

  function termsIn(text) {
    const lowered = (text || "").toLowerCase();
    return skillTerms.filter((term) => lowered.includes(term));
  }

  function metricsIn(text) {
    return (text || "")
      .split(/\n+/)
      .map((line) => line.trim().replace(/^-+\s*/, ""))
      .filter((line) => /\d/.test(line) && /%|\+|x|X|\$|years?|months?|releases?|stories?|wireframes?/i.test(line))
      .slice(0, 6);
  }

  function parseJD() {
    const raw = $("jd").value.trim();
    state.jdText = raw;
    if (!raw) {
      $("jd-parsed").textContent = "Paste or drop a JD first.";
      return null;
    }
    const terms = termsIn(raw);
    const firstLine = raw.split(/\n/).find(Boolean) || "Target role";
    state.parsedJD = {
      role: firstLine.slice(0, 90),
      must_have: terms.slice(0, 10),
      sector: terms.filter((t) => ["healthcare", "bfsi", "saas", "data", "platform"].includes(t)),
      tools: terms.filter((t) => ["snowflake", "fhir", "hl7", "api"].includes(t)),
    };
    $("jd-parsed").innerHTML = [
      `<div class="status-line"><span class="badge b-ok">Parsed</span><span>${state.parsedJD.role}</span></div>`,
      `<div>${state.parsedJD.must_have.map((t) => `<span class="chip">${t}</span>`).join("")}</div>`
    ].join("");
    buildQuestions();
    return state.parsedJD;
  }

  function buildQuestions() {
    const role = state.parsedJD?.role || "target role";
    state.questions = [
      ["Q1", "Business Impact", `What metrics prove fit for ${role}? Add cost, adoption, revenue, accuracy, CSAT, or speed.`],
      ["Q2", "Leadership", "What team size, stakeholder level, vendors, or cross-functional scope should be shown?"],
      ["Q3", "Technical Depth", "What architecture, API, data, AI, RAG, or platform trade-offs should be highlighted?"],
      ["Q4", "Discovery", "What interviews, UAT, experiments, workflow mapping, or validation evidence should be included?"],
      ["Q5", "Transformation", "What 0-to-1 launch, automation, migration, or operating model change proves impact?"],
    ];
    $("questions").innerHTML = state.questions.map(([id, category, prompt]) => `
      <label><strong>${id}. ${category}</strong><br><span class="dim">${prompt}</span>
      <textarea class="textarea answer-box" data-qid="${id}" placeholder="Optional. Auto mode can run without this, but answers improve quality."></textarea></label>
    `).join("");
  }

  function parseResumeText(text, name = "resume-context") {
    state.resumeText = text || "";
    state.resumeName = name;
    const skills = termsIn(state.resumeText);
    const metrics = metricsIn(state.resumeText);
    $("resume-preview").style.display = "block";
    $("resume-preview").textContent = [
      `Loaded: ${name}`,
      `Detected skills: ${skills.join(", ") || "none yet"}`,
      `Detected metrics: ${metrics.slice(0, 3).join(" | ") || "none yet"}`,
      "",
      state.resumeText.slice(0, 1200)
    ].join("\n");
  }

  function answers() {
    return Array.from(document.querySelectorAll("[data-qid]")).reduce((acc, el) => {
      if (el.value.trim()) acc[el.dataset.qid] = el.value.trim();
      return acc;
    }, {});
  }

  function selectedModel() {
    return document.querySelector('input[name="model"]:checked')?.value || "deterministic";
  }

  function generate() {
    const jd = state.parsedJD || parseJD();
    if (!jd) return;

    const resumeText = state.resumeText || "Product Manager with AI platform, RAG, API, roadmap, stakeholder, healthcare, BFSI, and SaaS experience.";
    const resumeSkills = termsIn(resumeText);
    const jdSkills = jd.must_have || [];
    const matched = unique(resumeSkills.filter((skill) => jdSkills.includes(skill)));
    const missing = unique(jdSkills.filter((skill) => !resumeSkills.includes(skill)));
    const metrics = metricsIn(resumeText);
    const answerMap = answers();
    const model = selectedModel();
    const llmPolish = model === "groq";

    const bullets = [
      metrics[0] ? `Delivered measurable outcome: ${metrics[0]}.` : "Owned roadmap and delivery for AI/data product initiatives with measurable business outcomes.",
      `Mapped JD priorities into proof points across ${unique([...matched, ...jdSkills]).slice(0, 7).join(", ")}.`,
      "Prepared application-ready narrative with provenance from resume context, JD requirements, and discovery answers.",
      ...Object.values(answerMap).slice(0, 3),
    ].slice(0, 6);

    const ats = Math.min(98, 72 + Math.round((matched.length / Math.max(jdSkills.length, 1)) * 24));
    const human = metrics.length ? 91 : 84;
    state.generated = { bullets, ats, human, matched, missing, model, llmPolish };

    $("results").style.display = "block";
    $("ats-score").textContent = `${ats}%`;
    $("human-score").textContent = `${human}%`;
    $("ats-breakdown").innerHTML = `Matched: ${matched.length}/${jdSkills.length}<br>Missing: ${missing.join(", ") || "none"}`;
    $("human-breakdown").innerHTML = `Metrics: ${metrics.length ? "present" : "needs more"}<br>LLM final polish: ${llmPolish ? "requested" : "off"}`;
    $("bullets").innerHTML = bullets.map((b) => `<li>${escapeHtml(b)}</li>`).join("");
    $("provenance").innerHTML = bullets.map((b, i) => `
      <tr><td>${escapeHtml(b)}</td><td>${i === 0 ? "resume_context" : i === 1 ? "jd_parser + gap_analysis" : "discovery/apply_package"}</td></tr>
    `).join("");
    $("apply-package").innerHTML = `
      <div class="apply-block">Recruiter note:
Hi, I am interested in this role. My background aligns with ${unique([...matched, ...jdSkills]).slice(0, 6).join(", ")}. I can share a tailored resume and would welcome a conversation.

Why this role:
This role fits my product experience across ${unique([...matched, ...jdSkills]).slice(0, 6).join(", ")} and my focus on measurable enterprise delivery.

Safety:
Draft only. Do not auto-submit. Confirm before filling external forms, uploading files, sending messages, or applying.</div>`;
    banner("Auto mode generated draft. Review before any external apply/save action.", true);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (ch) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    })[ch]);
  }

  function runAutoMode() {
    parseJD();
    generate();
  }

  function downloadMock() {
    const content = state.generated
      ? `# Tailored Resume Draft\n\n${state.generated.bullets.map((b) => `- ${b}`).join("\n")}\n`
      : "# Tailored Resume Draft\n\nRun auto mode first.\n";
    const blob = new Blob([content], { type: "text/markdown" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "tailored-resume-draft.md";
    a.click();
    URL.revokeObjectURL(a.href);
  }

  async function readFile(file) {
    if (!file) return;
    const textLike = /\.(md|txt|json|csv)$/i.test(file.name) || file.type.startsWith("text/");
    if (!textLike) {
      parseResumeText(`File selected: ${file.name}\nBinary parsing will run in backend phase. Paste markdown context for browser-only DnD auto mode.`, file.name);
      return;
    }
    parseResumeText(await file.text(), file.name);
  }

  function wireDrop(zone, handler) {
    zone.addEventListener("dragover", (event) => {
      event.preventDefault();
      zone.classList.add("dragover");
    });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
    zone.addEventListener("drop", async (event) => {
      event.preventDefault();
      zone.classList.remove("dragover");
      const file = event.dataTransfer.files?.[0];
      const text = event.dataTransfer.getData("text/plain");
      await handler(file, text);
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    $("resume-file").addEventListener("change", (event) => readFile(event.target.files[0]));
    wireDrop($("resume-drop"), async (file, text) => {
      if (file) await readFile(file);
      else if (text) parseResumeText(text, "dropped-text");
    });
    wireDrop($("jd-drop"), async (file, text) => {
      if (file && /\.(md|txt)$/i.test(file.name)) $("jd").value = await file.text();
      else if (text) $("jd").value = text;
      parseJD();
    });
    window.parseJD = parseJD;
    window.generate = generate;
    window.runAutoMode = runAutoMode;
    window.downloadMock = downloadMock;
  });
})();
