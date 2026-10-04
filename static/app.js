/**
 * ShieldSpam AI — Client Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {

  // --- STATE ---
  let currentChannel = 'sms';
  let presetsData = {};
  let batchData = [];
  let currentFilter = 'all';

  // --- DOM ELEMENTS ---
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  const domainOptions = document.querySelectorAll('.domain-option');
  const currentChannelBadge = document.getElementById('currentChannelBadge');
  const subjectGroup = document.getElementById('subjectGroup');
  const emailSubject = document.getElementById('emailSubject');
  const messageInput = document.getElementById('messageInput');
  const charCount = document.getElementById('charCount');
  const wordCount = document.getElementById('wordCount');
  const presetSpam = document.getElementById('presetSpam');
  const presetHam = document.getElementById('presetHam');
  const btnClear = document.getElementById('btnClear');
  const btnAnalyze = document.getElementById('btnAnalyze');

  // Results DOM
  const resultsEmpty = document.getElementById('resultsEmpty');
  const resultsActive = document.getElementById('resultsActive');
  const verdictBanner = document.getElementById('verdictBanner');
  const verdictIcon = document.getElementById('verdictIcon');
  const verdictTag = document.getElementById('verdictTag');
  const verdictTitle = document.getElementById('verdictTitle');
  const gaugeCircle = document.getElementById('gaugeCircle');
  const confidenceValue = document.getElementById('confidenceValue');
  const sigUrgency = document.getElementById('sigUrgency');
  const sigLinks = document.getElementById('sigLinks');
  const sigFinancial = document.getElementById('sigFinancial');
  const sigCaps = document.getElementById('sigCaps');
  const highlightContent = document.getElementById('highlightContent');
  const reasonsList = document.getElementById('reasonsList');

  // Batch DOM
  const dropZone = document.getElementById('dropZone');
  const csvFileInput = document.getElementById('csvFileInput');
  const btnSampleBatch = document.getElementById('btnSampleBatch');
  const batchResults = document.getElementById('batchResults');
  const sumTotal = document.getElementById('sumTotal');
  const sumSpam = document.getElementById('sumSpam');
  const sumHam = document.getElementById('sumHam');
  const sumRatio = document.getElementById('sumRatio');
  const batchTableBody = document.getElementById('batchTableBody');
  const btnExportCSV = document.getElementById('btnExportCSV');
  const filterChips = document.querySelectorAll('.filter-chip');

  // Analytics DOM
  const metricAcc = document.getElementById('metricAcc');
  const metricF1 = document.getElementById('metricF1');
  const metricPrec = document.getElementById('metricPrec');
  const metricRec = document.getElementById('metricRec');
  const cmTN = document.getElementById('cmTN');
  const cmFP = document.getElementById('cmFP');
  const cmFN = document.getElementById('cmFN');
  const cmTP = document.getElementById('cmTP');
  const algoComparisonBody = document.getElementById('algoComparisonBody');

  // --- INITIALIZATION ---
  fetchPresets();
  fetchMetrics();
  checkHealth();

  // --- TAB SWITCHING ---
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.getAttribute('data-tab');
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.add('hidden'));

      btn.classList.add('active');
      const targetTab = document.getElementById(`tab-${tabId}`);
      if (targetTab) targetTab.classList.remove('hidden');
    });
  });

  // --- DOMAIN SELECTOR ---
  domainOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      domainOptions.forEach(o => o.classList.remove('active'));
      opt.classList.add('active');

      const radio = opt.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;

      currentChannel = opt.getAttribute('data-channel');
      currentChannelBadge.textContent = `${currentChannel.toUpperCase()} Mode`;

      if (currentChannel === 'email') {
        subjectGroup.classList.remove('hidden');
      } else {
        subjectGroup.classList.add('hidden');
      }
    });
  });

  // --- TEXT COUNTERS ---
  messageInput.addEventListener('input', updateTextCounters);

  function updateTextCounters() {
    const text = messageInput.value || '';
    charCount.textContent = `${text.length} chars`;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    wordCount.textContent = `${words} words`;
  }

  // --- PRESETS LOADING ---
  async function fetchPresets() {
    try {
      const res = await fetch('/api/presets');
      if (res.ok) {
        presetsData = await res.json();
      }
    } catch (e) {
      console.warn("Could not fetch presets:", e);
    }
  }

  presetSpam.addEventListener('click', () => {
    if (!presetsData) return;
    if (currentChannel === 'sms') {
      messageInput.value = presetsData.sms_spam || '';
    } else if (currentChannel === 'email') {
      emailSubject.value = "URGENT: Inheritance Transfer of $14.5 Million USD";
      messageInput.value = presetsData.email_spam || '';
    } else {
      messageInput.value = presetsData.comment_spam || '';
    }
    updateTextCounters();
  });

  presetHam.addEventListener('click', () => {
    if (!presetsData) return;
    if (currentChannel === 'sms') {
      messageInput.value = presetsData.sms_ham || '';
    } else if (currentChannel === 'email') {
      emailSubject.value = "Q3 Financial Performance Review & Strategy Meeting Agenda";
      messageInput.value = presetsData.email_ham || '';
    } else {
      messageInput.value = presetsData.comment_ham || '';
    }
    updateTextCounters();
  });

  btnClear.addEventListener('click', () => {
    messageInput.value = '';
    emailSubject.value = '';
    updateTextCounters();
    resultsActive.classList.add('hidden');
    resultsEmpty.classList.remove('hidden');
  });

  // --- DETECT ACTION ---
  btnAnalyze.addEventListener('click', analyzeSingleMessage);

  messageInput.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
      analyzeSingleMessage();
    }
  });

  async function analyzeSingleMessage() {
    const text = messageInput.value.trim();
    if (!text) {
      alert("Please enter a message or load a preset sample.");
      return;
    }

    btnAnalyze.disabled = true;
    btnAnalyze.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Analyzing...`;

    try {
      const payload = {
        text: text,
        channel: currentChannel,
        subject: currentChannel === 'email' ? emailSubject.value.trim() : ''
      };

      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      renderResults(data);

    } catch (err) {
      console.error(err);
      alert("Error calling prediction API.");
    } finally {
      btnAnalyze.disabled = false;
      btnAnalyze.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Detect Spam <kbd>Ctrl + Enter</kbd>`;
    }
  }

  // --- RENDER RESULTS ---
  function renderResults(data) {
    resultsEmpty.classList.add('hidden');
    resultsActive.classList.remove('hidden');

    const isSpam = data.is_spam;
    const conf = data.confidence;
    const spamProb = data.spam_probability;

    // 1. Banner
    if (isSpam) {
      verdictBanner.className = 'verdict-banner is-spam';
      verdictIcon.innerHTML = `<i class="fa-solid fa-shield-virus"></i>`;
      verdictTag.textContent = 'SPAM DETECTED';
      verdictTitle.textContent = 'High-Risk Malicious Threat';
    } else {
      verdictBanner.className = 'verdict-banner is-ham';
      verdictIcon.innerHTML = `<i class="fa-solid fa-shield-check"></i>`;
      verdictTag.textContent = 'LEGITIMATE / SAFE';
      verdictTitle.textContent = 'No Threat Found';
    }

    // 2. Gauge Circle
    const pct = Math.round(spamProb * 100);
    const gaugeColor = isSpam ? '#f43f5e' : '#10b981';
    gaugeCircle.style.background = `conic-gradient(${gaugeColor} ${pct}%, rgba(255, 255, 255, 0.08) ${pct}%)`;
    confidenceValue.textContent = `${conf}%`;

    // 3. Signals Grid
    const meta = data.meta_features || {};
    sigUrgency.textContent = meta.urgency_score || 0;
    sigLinks.textContent = meta.url_count || 0;
    sigFinancial.textContent = meta.has_currency ? 'Yes' : 'No';
    sigCaps.textContent = `${Math.round((meta.uppercase_ratio || 0) * 100)}%`;

    // 4. XAI Highlights
    highlightContent.innerHTML = '';
    const tokens = data.highlights || [];
    tokens.forEach(tok => {
      const span = document.createElement('span');
      if (tok.risk === 'high') {
        span.className = 'hl-token risk-high';
        span.setAttribute('data-reason', tok.reason);
      } else if (tok.risk === 'medium') {
        span.className = 'hl-token risk-medium';
        span.setAttribute('data-reason', tok.reason);
      } else {
        span.className = 'hl-token';
      }
      span.textContent = tok.text;
      highlightContent.appendChild(span);
    });

    // 5. Reasons list
    reasonsList.innerHTML = '';
    const reasons = data.risk_reasons || [];
    reasons.forEach(r => {
      const li = document.createElement('li');
      li.textContent = r;
      reasonsList.appendChild(li);
    });
  }

  // --- BATCH SCANNER ---
  btnSampleBatch.addEventListener('click', runDemoBatch);

  async function runDemoBatch() {
    const sampleItems = [
      { text: "URGENT! You have won a $1,000 Walmart Gift Card. Click http://bit.ly/claim now!", channel: "sms" },
      { text: "Hey Alex, are we still meeting for lunch at 12:30 PM?", channel: "sms" },
      { text: "Subject: Inheritance Transfer of $14.5 Million USD\nDear Friend, I am Mr. Abacha...", channel: "email" },
      { text: "Subject: Q3 Financial Review Agenda\nHi Team, Attached is the draft agenda...", channel: "email" },
      { text: "Make $15,000 in one month trading forex! Contact WhatsApp +1-987-654-3210", channel: "comment" },
      { text: "This tutorial was super clear and helpful! Loved the explanation.", channel: "comment" },
      { text: "BUY CHEAP XANAX VALIUM WITHOUT PRESCRIPTION FAST SHIPPING http://meds-cheap.ru", channel: "comment" },
      { text: "Your verification code for Google is 482019. Do not share.", channel: "sms" },
      { text: "Subject: Account Suspended\nYour PayPal account has been restricted. Verify now at http://paypal-fake.com", channel: "email" },
      { text: "Don't forget to bring your passport and boarding pass tomorrow!", channel: "sms" }
    ];

    btnSampleBatch.disabled = true;
    btnSampleBatch.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Processing...`;

    try {
      const res = await fetch('/api/batch-predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: sampleItems })
      });

      const data = await res.json();
      renderBatchResults(data);

    } catch (e) {
      alert("Batch processing error.");
    } finally {
      btnSampleBatch.disabled = false;
      btnSampleBatch.innerHTML = `<i class="fa-solid fa-vial"></i> Load Demo Batch (20 Messages)`;
    }
  }

  // CSV Drag and drop / file upload
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('hover');
  });

  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('hover'));

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('hover');
    if (e.dataTransfer.files.length) {
      handleCsvFile(e.dataTransfer.files[0]);
    }
  });

  csvFileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
      handleCsvFile(e.target.files[0]);
    }
  });

  function handleCsvFile(file) {
    const reader = new FileReader();
    reader.onload = async (evt) => {
      const text = evt.target.result;
      const lines = text.split(/\r?\n/).filter(line => line.trim());
      const messages = lines.map(line => {
        // Strip leading quotes if CSV line
        const cleaned = line.replace(/^"|"$/g, '').trim();
        return { text: cleaned, channel: 'sms' };
      });

      if (!messages.length) return;

      try {
        const res = await fetch('/api/batch-predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ messages })
        });
        const data = await res.json();
        renderBatchResults(data);
      } catch (err) {
        alert("Failed to parse & scan CSV file.");
      }
    };
    reader.readAsText(file);
  }

  function renderBatchResults(data) {
    batchResults.classList.remove('hidden');
    batchData = data.results || [];

    sumTotal.textContent = data.total;
    sumSpam.textContent = data.spam_count;
    sumHam.textContent = data.ham_count;
    sumRatio.textContent = `${data.spam_ratio}%`;

    renderTableRows();
  }

  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentFilter = chip.getAttribute('data-filter');
      renderTableRows();
    });
  });

  function renderTableRows() {
    batchTableBody.innerHTML = '';
    const filtered = batchData.filter(item => {
      if (currentFilter === 'spam') return item.is_spam;
      if (currentFilter === 'ham') return !item.is_spam;
      return true;
    });

    filtered.forEach(item => {
      const tr = document.createElement('tr');
      const preview = item.text.length > 70 ? item.text.substring(0, 70) + '...' : item.text;
      
      tr.innerHTML = `
        <td>${item.id}</td>
        <td><span class="badge channel-badge">${item.channel.toUpperCase()}</span></td>
        <td>${escapeHtml(preview)}</td>
        <td>${item.is_spam ? '<span class="badge-spam">SPAM</span>' : '<span class="badge-ham">SAFE</span>'}</td>
        <td><strong>${item.confidence}%</strong></td>
        <td>${item.meta_features.urgency_score}</td>
      `;
      batchTableBody.appendChild(tr);
    });
  }

  // Export CSV
  btnExportCSV.addEventListener('click', () => {
    if (!batchData.length) return;
    let csv = "ID,Channel,Message,Label,Confidence,UrgencyScore\n";
    batchData.forEach(item => {
      const textClean = `"${item.text.replace(/"/g, '""')}"`;
      csv += `${item.id},${item.channel},${textClean},${item.label},${item.confidence}%,${item.meta_features.urgency_score}\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `ShieldSpam_Results_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  // --- ANALYTICS TAB ---
  async function fetchMetrics() {
    try {
      const res = await fetch('/api/metrics');
      if (res.ok) {
        const data = await res.json();
        metricAcc.textContent = `${(data.accuracy * 100).toFixed(1)}%`;
        metricF1.textContent = `${(data.f1_score * 100).toFixed(1)}%`;
        metricPrec.textContent = `${(data.precision * 100).toFixed(1)}%`;
        metricRec.textContent = `${(data.recall * 100).toFixed(1)}%`;

        const cm = data.confusion_matrix || {};
        cmTN.textContent = cm.tn || 0;
        cmFP.textContent = cm.fp || 0;
        cmFN.textContent = cm.fn || 0;
        cmTP.textContent = cm.tp || 0;

        // Model comparison table
        algoComparisonBody.innerHTML = '';
        const algos = data.model_comparison || {};
        Object.keys(algos).forEach(name => {
          const item = algos[name];
          const tr = document.createElement('tr');
          const isActive = name.includes('Active');
          tr.innerHTML = `
            <td><strong>${name}</strong></td>
            <td>NLP Classifier</td>
            <td>${(item.accuracy * 100).toFixed(1)}%</td>
            <td>${(item.f1_score * 100).toFixed(1)}%</td>
            <td>${isActive ? '<span class="badge-ham">ACTIVE</span>' : '<span class="badge channel-badge">EVALUATED</span>'}</td>
          `;
          algoComparisonBody.appendChild(tr);
        });
      }
    } catch (err) {
      console.warn("Could not load metrics:", err);
    }
  }

  // --- HEALTH CHECK ---
  async function checkHealth() {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        document.getElementById('apiStatus').style.display = 'flex';
      }
    } catch (e) {
      console.warn("API health check failed.");
    }
  }

  function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

});
