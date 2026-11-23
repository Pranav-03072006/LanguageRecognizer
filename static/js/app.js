/**
 * PolyGlot AI - Frontend Application Logic
 * Pure Vanilla JavaScript (No heavy frameworks, fetch API, live counters, localStorage history)
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const textInput = document.getElementById('text-input');
    const detectBtn = document.getElementById('detect-btn');
    const detectBtnText = document.getElementById('detect-btn-text');
    const detectSpinner = document.getElementById('detect-spinner');
    const clearBtn = document.getElementById('clear-btn');
    const randomSampleBtn = document.getElementById('random-sample-btn');
    const sampleChipsContainer = document.getElementById('sample-chips-container');
    const errorBanner = document.getElementById('error-banner');
    const errorMessage = document.getElementById('error-message');

    // Counters
    const liveCharCount = document.getElementById('live-char-count');
    const liveWordCount = document.getElementById('live-word-count');
    const liveLineCount = document.getElementById('live-line-count');
    const detectedScriptBadge = document.getElementById('detected-script-badge');
    const liveScriptName = document.getElementById('live-script-name');

    // Results Display
    const resultsPlaceholder = document.getElementById('results-placeholder');
    const resultsContainer = document.getElementById('results-container');
    const meaningCard = document.getElementById('meaning-card');
    const meaningNativeScript = document.getElementById('meaning-native-script');
    const meaningTranslationText = document.getElementById('meaning-translation-text');
    const meaningExplanationText = document.getElementById('meaning-explanation-text');
    const predictedLanguageName = document.getElementById('predicted-language-name');
    const predictedNativeName = document.getElementById('predicted-native-name');
    const confidenceBadge = document.getElementById('confidence-badge');
    const confidenceScore = document.getElementById('confidence-score');
    const resCharCount = document.getElementById('res-char-count');
    const resWordCount = document.getElementById('res-word-count');
    const resScript = document.getElementById('res-script');
    const probabilitiesList = document.getElementById('probabilities-list');

    // AI Insights Elements
    const aiSourceBadge = document.getElementById('ai-source-badge');
    const aiFamily = document.getElementById('ai-family');
    const aiScript = document.getElementById('ai-script');
    const aiSpeakers = document.getElementById('ai-speakers');
    const aiSpeakersRow = document.getElementById('ai-speakers-row');
    const aiTraits = document.getElementById('ai-traits');
    const aiOverview = document.getElementById('ai-overview');
    const aiTranslation = document.getElementById('ai-translation');
    const aiTranslationSection = document.getElementById('ai-translation-section');
    const aiFunfact = document.getElementById('ai-funfact');
    const aiProviderText = document.getElementById('ai-provider-text');
    const aiStatusNote = document.getElementById('ai-status-note');

    // History Elements
    const historyList = document.getElementById('history-list');
    const historyEmpty = document.getElementById('history-empty');
    const clearHistoryBtn = document.getElementById('clear-history-btn');

    // Gemini API Key Modal Elements
    const llmKeyBtn = document.getElementById('llm-key-btn');
    const llmStatusLabel = document.getElementById('llm-status-label');
    const apiKeyModal = document.getElementById('api-key-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const cancelModalBtn = document.getElementById('cancel-modal-btn');
    const saveApiKeyBtn = document.getElementById('save-api-key-btn');
    const removeApiKeyBtn = document.getElementById('remove-api-key-btn');
    const geminiApiKeyInput = document.getElementById('gemini-api-key-input');

    const STORAGE_KEY = 'polyglot_detection_history';
    const GEMINI_KEY_STORAGE = 'polyglot_gemini_api_key';

    // -------------------------------------------------------------
    // Gemini API Key Management
    // -------------------------------------------------------------
    function updateApiKeyUI() {
        const key = localStorage.getItem(GEMINI_KEY_STORAGE) || '';
        if (llmStatusLabel && llmKeyBtn) {
            if (key) {
                llmStatusLabel.textContent = 'LLM: Gemini (Connected)';
                llmKeyBtn.className = 'flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all shadow-sm cursor-pointer border hover:shadow-md bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100';
                const svg = llmKeyBtn.querySelector('svg');
                if (svg) svg.className = 'w-3.5 h-3.5 text-emerald-600';
            } else {
                llmStatusLabel.textContent = 'LLM: Gemini (Click to Add Key)';
                llmKeyBtn.className = 'flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all shadow-sm cursor-pointer border hover:shadow-md bg-amber-50 text-amber-800 border-amber-300 hover:bg-amber-100';
                const svg = llmKeyBtn.querySelector('svg');
                if (svg) svg.className = 'w-3.5 h-3.5 text-amber-600';
            }
        }
    }

    if (llmKeyBtn && apiKeyModal) {
        llmKeyBtn.addEventListener('click', () => {
            geminiApiKeyInput.value = localStorage.getItem(GEMINI_KEY_STORAGE) || '';
            apiKeyModal.classList.remove('hidden');
            geminiApiKeyInput.focus();
        });

        const closeModal = () => apiKeyModal.classList.add('hidden');
        if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
        if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeModal);
        apiKeyModal.addEventListener('click', (e) => {
            if (e.target === apiKeyModal) closeModal();
        });

        if (saveApiKeyBtn) {
            saveApiKeyBtn.addEventListener('click', () => {
                const val = geminiApiKeyInput.value.trim();
                if (val) {
                    localStorage.setItem(GEMINI_KEY_STORAGE, val);
                } else {
                    localStorage.removeItem(GEMINI_KEY_STORAGE);
                }
                updateApiKeyUI();
                closeModal();
                // If there is text in input, auto re-run detection with new key
                if (textInput.value.trim()) {
                    performDetection();
                }
            });
        }

        if (removeApiKeyBtn) {
            removeApiKeyBtn.addEventListener('click', () => {
                localStorage.removeItem(GEMINI_KEY_STORAGE);
                geminiApiKeyInput.value = '';
                updateApiKeyUI();
                closeModal();
            });
        }
    }

    updateApiKeyUI();

    // -------------------------------------------------------------
    // Helper: CSRF Token Cookie Retrieval
    // -------------------------------------------------------------
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // -------------------------------------------------------------
    // Quick Client-Side Script Detector for Live Indicator
    // -------------------------------------------------------------
    function detectScriptClient(text) {
        if (!text || !text.trim()) return null;
        if (/[\u0400-\u04FF]/.test(text)) return 'Cyrillic';
        if (/[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]/.test(text)) return 'Arabic/Persian/Urdu';
        if (/[\u0900-\u097F]/.test(text)) return 'Devanagari';
        if (/[\u0B80-\u0BFF]/.test(text)) return 'Tamil';
        if (/[\u0E00-\u0E7F]/.test(text)) return 'Thai';
        if (/[\u3040-\u30FF]/.test(text)) return 'Japanese Kana';
        if (/[\u4E00-\u9FFF]/.test(text)) return 'Chinese Hanzi';
        if (/[\uAC00-\uD7AF\u1100-\u11FF]/.test(text)) return 'Korean Hangul';
        if (/[A-Za-z\u00C0-\u024F]/.test(text)) return 'Latin';
        return 'Standard';
    }

    // -------------------------------------------------------------
    // Live Text Statistics Updater
    // -------------------------------------------------------------
    function updateCounters() {
        const text = textInput.value;
        const charCount = text.length;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const lines = text ? text.split(/\r\n|\r|\n/).length : 0;

        liveCharCount.textContent = charCount.toLocaleString();
        liveWordCount.textContent = words.toLocaleString();
        liveLineCount.textContent = lines.toLocaleString();

        const script = detectScriptClient(text);
        if (script) {
            detectedScriptBadge.classList.remove('hidden');
            detectedScriptBadge.classList.add('inline-flex');
            liveScriptName.textContent = script;
        } else {
            detectedScriptBadge.classList.add('hidden');
            detectedScriptBadge.classList.remove('inline-flex');
        }
    }

    textInput.addEventListener('input', updateCounters);

    // -------------------------------------------------------------
    // Sample Chips Handler
    // -------------------------------------------------------------
    if (sampleChipsContainer) {
        sampleChipsContainer.addEventListener('click', (e) => {
            const chip = e.target.closest('.sample-chip');
            if (!chip) return;
            const text = chip.getAttribute('data-text');
            if (text) {
                textInput.value = text;
                updateCounters();
                hideError();
                // Auto trigger detection for snappy UX
                performDetection();
            }
        });
    }

    // Random Sample Button
    if (randomSampleBtn) {
        randomSampleBtn.addEventListener('click', () => {
            const chips = document.querySelectorAll('.sample-chip');
            if (!chips.length) return;
            const randomIndex = Math.floor(Math.random() * chips.length);
            const selectedChip = chips[randomIndex];
            textInput.value = selectedChip.getAttribute('data-text') || '';
            updateCounters();
            hideError();
            performDetection();
        });
    }

    // Clear Button
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            textInput.value = '';
            updateCounters();
            hideError();
            textInput.focus();
        });
    }

    // Keyboard Shortcut: Ctrl + Enter / Cmd + Enter
    textInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            performDetection();
        }
    });

    if (detectBtn) {
        detectBtn.addEventListener('click', performDetection);
    }

    // -------------------------------------------------------------
    // Error Handling Helpers
    // -------------------------------------------------------------
    function showError(msg) {
        errorMessage.textContent = msg;
        errorBanner.classList.remove('hidden');
        errorBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideError() {
        errorBanner.classList.add('hidden');
    }

    // -------------------------------------------------------------
    // Core Detection AJAX Call
    // -------------------------------------------------------------
    async function performDetection() {
        const text = textInput.value.trim();
        if (!text) {
            showError('Please type or paste some text first, or click one of the sample chips.');
            textInput.focus();
            return;
        }

        hideError();
        setLoading(true);

        try {
            const csrftoken = getCookie('csrftoken');
            const storedKey = localStorage.getItem(GEMINI_KEY_STORAGE) || '';
            const response = await fetch('/api/detect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken || '',
                },
                body: JSON.stringify({
                    text: text,
                    api_key: storedKey,
                }),
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || `Server responded with status ${response.status}`);
            }

            renderResults(data);
            saveToHistory(data);
        } catch (err) {
            console.error('Detection request error:', err);
            showError(err.message || 'Network error occurred while contacting the server.');
        } finally {
            setLoading(false);
        }
    }

    function setLoading(isLoading) {
        if (isLoading) {
            detectBtn.disabled = true;
            detectSpinner.classList.remove('hidden');
            detectBtnText.textContent = 'Analyzing...';
        } else {
            detectBtn.disabled = false;
            detectSpinner.classList.add('hidden');
            detectBtnText.textContent = 'Detect Language';
        }
    }

    // -------------------------------------------------------------
    // Results Renderer
    // -------------------------------------------------------------
    function renderResults(data) {
        // Toggle view from placeholder to active results
        resultsPlaceholder.classList.add('hidden');
        resultsContainer.classList.remove('hidden');
        resultsContainer.classList.add('animate-fade-in');

        const pred = data.prediction || {};
        const stats = data.stats || {};
        const ai = data.ai_insights || {};
        const meaning = data.meaning || {};

        // 0. Word / Phrase / Sentence Meaning Card
        const translation = meaning.translation || ai.translation_or_gist || '';
        const nativeScript = meaning.native_script || ai.word_native_script || ai.native_name || '';
        const explanation = meaning.explanation || ai.overview || '';

        if (translation && !translation.includes('Translation requires active LLM API key')) {
            if (meaningCard) {
                meaningCard.classList.remove('hidden');
                const wordsCount = (data.text || textInput.value || '').trim().split(/\s+/).length;
                const meaningTag = meaningCard.querySelector('span');
                if (meaningTag) {
                    meaningTag.textContent = wordsCount > 1 ? 'Sentence Meaning & Translation' : 'Word / Phrase Meaning';
                }
                meaningTranslationText.textContent = `"${translation}"`;
                meaningNativeScript.textContent = nativeScript || (wordsCount > 1 ? `${pred.language} Text` : pred.language);
                meaningExplanationText.textContent = explanation;
            }
        } else {
            if (meaningCard) {
                meaningCard.classList.add('hidden');
            }
        }

        // 1. Primary Prediction Card
        predictedLanguageName.textContent = pred.language || 'Unknown';
        predictedNativeName.textContent = ai.native_name || '';

        const confidence = pred.confidence || 0;
        confidenceScore.textContent = `${confidence.toFixed(1)}%`;

        // Confidence badge color tuning
        confidenceBadge.className = 'px-2.5 py-1 rounded-full text-xs font-semibold border ' +
            (confidence >= 80 ? 'bg-emerald-100 text-emerald-800 border-emerald-200' :
             confidence >= 50 ? 'bg-amber-100 text-amber-800 border-amber-200' :
             'bg-rose-100 text-rose-800 border-rose-200');

        // Text statistics
        resCharCount.textContent = (stats.char_count || 0).toLocaleString();
        resWordCount.textContent = (stats.word_count || 0).toLocaleString();
        resScript.textContent = stats.detected_script || 'Standard';

        // 2. Probabilities Breakdown
        probabilitiesList.innerHTML = '';
        const topProbs = pred.top_probabilities || [];
        topProbs.forEach((item, index) => {
            const prob = item.probability || 0;
            const isTop = index === 0;

            const row = document.createElement('div');
            row.className = 'space-y-1';
            row.innerHTML = `
                <div class="flex items-center justify-between text-xs font-medium">
                    <span class="${isTop ? 'font-bold text-indigo-900' : 'text-slate-700'}">${escapeHtml(item.language)}</span>
                    <span class="${isTop ? 'font-bold text-indigo-700' : 'text-slate-500'}">${prob.toFixed(1)}%</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div class="prob-bar-fill h-2 rounded-full ${isTop ? 'bg-indigo-600' : 'bg-slate-300'}" style="width: 0%"></div>
                </div>
            `;
            probabilitiesList.appendChild(row);

            // Animate bar width smoothly
            setTimeout(() => {
                const fill = row.querySelector('.prob-bar-fill');
                if (fill) fill.style.width = `${Math.max(prob, 1)}%`;
            }, 50 + index * 40);
        });

        // 3. AI Insights Card
        if (ai.source === 'llm') {
            aiSourceBadge.textContent = 'Live LLM Insight';
            aiSourceBadge.className = 'px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200';
            aiProviderText.textContent = `${ai.provider || 'LLM'} (${ai.model || 'Direct SDK'})`;
            aiStatusNote.textContent = 'Live Generated';
        } else {
            aiSourceBadge.textContent = 'Linguistic Knowledge Base';
            aiSourceBadge.className = 'px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-100 text-amber-800 border border-amber-200';
            aiProviderText.textContent = 'Curated Linguistic Profile (No API Key Required)';
            aiStatusNote.textContent = 'Verified Offline Fallback';
        }

        aiFamily.textContent = ai.language_family || 'Not specified';
        aiScript.textContent = ai.writing_script || 'Standard';

        if (ai.speakers_estimate) {
            aiSpeakersRow.classList.remove('hidden');
            aiSpeakers.textContent = ai.speakers_estimate;
        } else {
            aiSpeakersRow.classList.add('hidden');
        }

        aiTraits.textContent = ai.linguistic_features || 'Canonical grammatical structure';
        aiOverview.textContent = ai.overview || 'Linguistic overview available.';

        if (ai.translation_or_gist) {
            aiTranslationSection.classList.remove('hidden');
            aiTranslation.textContent = `“${ai.translation_or_gist}”`;
        } else {
            aiTranslationSection.classList.add('hidden');
        }

        if (ai.fun_fact) {
            aiFunfact.textContent = ai.fun_fact;
        } else {
            aiFunfact.textContent = `${pred.language} is recognized for its unique structural characteristics.`;
        }
    }

    // -------------------------------------------------------------
    // History Management via localStorage
    // -------------------------------------------------------------
    function loadHistory() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            const history = raw ? JSON.parse(raw) : [];
            renderHistoryUI(history);
        } catch (e) {
            console.warn('Failed to parse history from localStorage', e);
            renderHistoryUI([]);
        }
    }

    function saveToHistory(data) {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            let history = raw ? JSON.parse(raw) : [];

            const item = {
                id: Date.now(),
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                text: data.text,
                language: data.prediction ? data.prediction.language : 'Unknown',
                confidence: data.prediction ? data.prediction.confidence : 0,
                fullData: data,
            };

            // Prepend, keep up to 12 recent items
            history = [item, ...history.filter(h => h.text !== data.text)].slice(0, 12);
            localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
            renderHistoryUI(history);
        } catch (e) {
            console.warn('Failed to save to localStorage', e);
        }
    }

    function renderHistoryUI(history) {
        if (!history || history.length === 0) {
            historyEmpty.classList.remove('hidden');
            historyList.classList.add('hidden');
            return;
        }

        historyEmpty.classList.add('hidden');
        historyList.classList.remove('hidden');
        historyList.innerHTML = '';

        history.forEach(item => {
            const el = document.createElement('div');
            el.className = 'history-item p-2.5 rounded-xl border border-slate-100 hover:border-indigo-200 bg-slate-50/50 hover:bg-indigo-50/40 cursor-pointer flex items-center justify-between gap-3 text-xs';
            el.innerHTML = `
                <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-0.5">
                        <span class="font-semibold text-slate-800">${escapeHtml(item.language)}</span>
                        <span class="text-[10px] text-slate-400">${item.confidence ? item.confidence.toFixed(0) + '%' : ''}</span>
                        <span class="text-[10px] text-slate-400">&bull; ${item.timestamp || ''}</span>
                    </div>
                    <p class="text-slate-500 truncate font-mono text-[11px]">${escapeHtml(item.text)}</p>
                </div>
                <svg class="w-4 h-4 text-slate-300 hover:text-indigo-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
            `;

            // Click-to-reload
            el.addEventListener('click', () => {
                textInput.value = item.text;
                updateCounters();
                hideError();
                if (item.fullData) {
                    renderResults(item.fullData);
                } else {
                    performDetection();
                }
            });

            historyList.appendChild(el);
        });
    }

    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', () => {
            localStorage.removeItem(STORAGE_KEY);
            renderHistoryUI([]);
        });
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Initialize
    updateCounters();
    loadHistory();
});
