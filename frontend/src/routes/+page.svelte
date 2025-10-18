<script lang="ts">
	import { onMount } from 'svelte';
	
	let mediaRecorder: MediaRecorder | null = null;
	let socket: WebSocket | null = null;
	let suggestions: string[] = [];
	let ideaSuggestions: string[] = [];
	let aiTags: string[] = [];
	let confidenceLevel = 0;
	let isRecording = false;
	let isListening = false;
	let audioLevel = 0;
	let currentTranscript = '';
	let fullTranscript = '';
	let mindMapNodes: Array<{id: string, text: string, x: number, y: number, connections: string[], highlighted?: boolean}> = [];
	let settingsOpen = false;
	let tagsOpen = false;
	let selectedTags: string[] = [];
	let availableTags = ['AI', 'Technology', 'Business', 'Creative', 'Research', 'Meeting', 'Ideas'];
	let currentTheme = 'dark';
	let currentLanguage = 'en';
	let testMode = false;
	let listeningTimer: number | null = null;
	let uploadedFile = null;
	let uploadedText = '';
	let documentContext = '';
	let isAnalyzingDocument = false;
	
	// Professional settings
	let tagCreationCount = 3;
	let ideaCount = 5;
	let confidenceThreshold = 70;
	let autoTagging = true;
	let ideaFiltering = true;
	let suggestionCooldown = 3; // seconds
	
	// Backend URL - can be configured via environment variable
	const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

	// Speech Recognition Settings
	let speechSettings = {
		language: 'en-US',
		confidenceThreshold: 0.7,
		useGoogleCloud: false,
		fallbackToOffline: true,
		audioFormat: 'webm',
		sampleRate: 44100,
		channels: 1
	};

	// Browser Speech Recognition
	let recognition: any = null;
	let speechText = '';
	let speechTextArea: HTMLTextAreaElement | null = null;
	let sessionStats = {
		totalIdeas: 0,
		totalTags: 0,
		confidenceAvg: 0,
		sessionTime: 0
	};
	let themes = {
		dark: { bg: '#0a0a0a', text: '#00ff00', accent: '#00ff00', secondary: '#333', name: 'Matrix Dark' },
		light: { bg: '#ffffff', text: '#000000', accent: '#0066cc', secondary: '#f0f0f0', name: 'Clean Light' },
		cyber: { bg: '#000011', text: '#00ffff', accent: '#ff00ff', secondary: '#001122', name: 'Cyber Punk' },
		neon: { bg: '#0d1117', text: '#39ff14', accent: '#ff0080', secondary: '#161b22', name: 'Neon Glow' },
		solar: { bg: '#1a1a2e', text: '#ffd700', accent: '#ff6b35', secondary: '#16213e', name: 'Solar Flare' },
		ocean: { bg: '#001122', text: '#00d4ff', accent: '#00ff88', secondary: '#002244', name: 'Deep Ocean' },
		forest: { bg: '#0d1b0d', text: '#00ff41', accent: '#ffaa00', secondary: '#1a2e1a', name: 'Digital Forest' },
		cosmic: { bg: '#0f0f23', text: '#e94560', accent: '#f5a623', secondary: '#1a1a3a', name: 'Cosmic Purple' },
		steel: { bg: '#1e1e1e', text: '#c0c0c0', accent: '#ff4444', secondary: '#2d2d2d', name: 'Steel Gray' },
		aurora: { bg: '#0a0a0f', text: '#00ffcc', accent: '#ff3366', secondary: '#1a1a2e', name: 'Aurora Borealis' },
		midnight: { bg: '#000000', text: '#ffffff', accent: '#ff0080', secondary: '#1a1a1a', name: 'Midnight Blue' },
		sunset: { bg: '#2d1b69', text: '#ff6b6b', accent: '#4ecdc4', secondary: '#3d2a7a', name: 'Sunset Gradient' },
		emerald: { bg: '#0d2818', text: '#00ff88', accent: '#ffd700', secondary: '#1a3d2a', name: 'Emerald City' },
		volcanic: { bg: '#1a0d0d', text: '#ff4444', accent: '#ffaa00', secondary: '#2d1a1a', name: 'Volcanic Red' },
		arctic: { bg: '#f0f8ff', text: '#0066cc', accent: '#00aaff', secondary: '#e6f3ff', name: 'Arctic Blue' },
		lavender: { bg: '#2d1b69', text: '#e6e6fa', accent: '#ff69b4', secondary: '#3d2a7a', name: 'Lavender Dreams' }
	};

	// Multi-language support
	const translations = {
		en: {
			appName: 'NextWord',
			ready: 'READY',
			listening: 'LISTENING',
			aiAnalyzing: 'AI is analyzing your speech...',
			waitingForSpeech: 'Listening for speech...',
			audioControl: 'Audio Control',
			startRecording: 'Start Recording',
			stopRecording: 'Stop Recording',
			audioLevel: 'Audio Level',
			liveTranscript: 'Live Transcript',
			current: 'Current',
			fullSession: 'Full Session',
			startSpeaking: 'Start speaking to see your words here...',
			aiSuggestions: 'AI Suggestions',
			aiSuggestionsPlaceholder: 'AI suggestions will appear here...',
			documentContext: 'Document Context',
			uploadDocument: 'Upload Document',
			pasteText: 'Or paste your text here for AI analysis...',
			analyzeText: 'Analyze Text',
			documentPreview: 'Document Context:',
			clear: 'Clear',
			analyzingDocument: 'AI is analyzing your document...',
			topicTags: 'Topic Tags',
			topicTagsPlaceholder: 'Topic tags will appear here...',
			aiConfidence: 'AI Confidence',
			sessionStats: 'Session Stats',
			ideasGenerated: 'Ideas Generated:',
			tagsCreated: 'Tags Created:',
			avgConfidence: 'Avg Confidence:',
			professionalSettings: 'Professional Settings',
			aiBehavior: 'AI Behavior',
			tagCreationCount: 'Tag Creation Count',
			ideaCount: 'Idea Count',
			confidenceThreshold: 'Confidence Threshold',
			suggestionCooldown: 'Suggestion Cooldown',
			features: 'Features',
			autoTagging: 'Auto Tagging',
			ideaFiltering: 'Idea Filtering',
			appearance: 'Appearance',
			theme: 'Theme',
			speechRecognition: 'Speech Recognition',
			language: 'Language',
			speechConfidence: 'Speech Confidence',
			useGoogleCloud: 'Use Google Cloud',
			fallbackOffline: 'Fallback to Offline',
			audioFormat: 'Audio Format',
			sampleRate: 'Sample Rate',
			channels: 'Channels',
			sessionTags: 'Session Tags',
			activeTags: 'Active Tags:',
			nextIdeas: 'Next Ideas:',
			explore: 'Explore',
			continueTalking: 'Click to continue talking about',
			clickToExplore: 'Click to explore',
			debug: 'Debug',
			recording: 'Recording',
			websocket: 'WebSocket',
			testMode: 'Test Mode',
			on: 'On',
			off: 'Off',
			connected: 'Connected',
			disconnected: 'Disconnected',
			yes: 'Yes',
			no: 'No',
			yourThoughts: 'Your Thoughts'
		},
		de: {
			appName: 'NextWord',
			ready: 'BEREIT',
			listening: 'HÖRT ZU',
			aiAnalyzing: 'KI analysiert Ihre Sprache...',
			waitingForSpeech: 'Warte auf Sprache...',
			audioControl: 'Audio-Steuerung',
			startRecording: 'Aufnahme starten',
			stopRecording: 'Aufnahme stoppen',
			audioLevel: 'Audio-Level',
			liveTranscript: 'Live-Transkript',
			current: 'Aktuell',
			fullSession: 'Vollständige Sitzung',
			startSpeaking: 'Beginnen Sie zu sprechen, um Ihre Wörter hier zu sehen...',
			aiSuggestions: 'KI-Vorschläge',
			aiSuggestionsPlaceholder: 'KI-Vorschläge erscheinen hier...',
			documentContext: 'Dokument-Kontext',
			uploadDocument: 'Dokument hochladen',
			pasteText: 'Oder fügen Sie Ihren Text hier zur KI-Analyse ein...',
			analyzeText: 'Text analysieren',
			documentPreview: 'Dokument-Kontext:',
			clear: 'Löschen',
			analyzingDocument: 'KI analysiert Ihr Dokument...',
			topicTags: 'Themen-Tags',
			topicTagsPlaceholder: 'Themen-Tags erscheinen hier...',
			aiConfidence: 'KI-Vertrauen',
			sessionStats: 'Sitzungs-Statistiken',
			ideasGenerated: 'Ideen generiert:',
			tagsCreated: 'Tags erstellt:',
			avgConfidence: 'Durchschn. Vertrauen:',
			professionalSettings: 'Professionelle Einstellungen',
			aiBehavior: 'KI-Verhalten',
			tagCreationCount: 'Tag-Erstellungsanzahl',
			ideaCount: 'Ideen-Anzahl',
			confidenceThreshold: 'Vertrauens-Schwellenwert',
			suggestionCooldown: 'Vorschlags-Abkühlzeit',
			features: 'Funktionen',
			autoTagging: 'Auto-Tagging',
			ideaFiltering: 'Ideen-Filterung',
			appearance: 'Erscheinungsbild',
			theme: 'Design',
			sessionTags: 'Sitzungs-Tags',
			activeTags: 'Aktive Tags:',
			nextIdeas: 'Nächste Ideen:',
			explore: 'Erkunden',
			continueTalking: 'Klicken Sie, um über',
			clickToExplore: 'Klicken Sie, um zu erkunden',
			debug: 'Debug',
			recording: 'Aufnahme',
			websocket: 'WebSocket',
			testMode: 'Test-Modus',
			on: 'An',
			off: 'Aus',
			connected: 'Verbunden',
			disconnected: 'Getrennt',
			yes: 'Ja',
			no: 'Nein',
			yourThoughts: 'Ihre Gedanken'
		},
		fr: {
			appName: 'NextWord',
			ready: 'PRÊT',
			listening: 'ÉCOUTE',
			aiAnalyzing: 'L\'IA analyse votre discours...',
			waitingForSpeech: 'En attente de parole...',
			audioControl: 'Contrôle audio',
			startRecording: 'Commencer l\'enregistrement',
			stopRecording: 'Arrêter l\'enregistrement',
			audioLevel: 'Niveau audio',
			liveTranscript: 'Transcription en direct',
			current: 'Actuel',
			fullSession: 'Session complète',
			startSpeaking: 'Commencez à parler pour voir vos mots ici...',
			aiSuggestions: 'Suggestions IA',
			aiSuggestionsPlaceholder: 'Les suggestions IA apparaîtront ici...',
			documentContext: 'Contexte du document',
			uploadDocument: 'Télécharger un document',
			pasteText: 'Ou collez votre texte ici pour l\'analyse IA...',
			analyzeText: 'Analyser le texte',
			documentPreview: 'Contexte du document:',
			clear: 'Effacer',
			analyzingDocument: 'L\'IA analyse votre document...',
			topicTags: 'Tags de sujet',
			topicTagsPlaceholder: 'Les tags de sujet apparaîtront ici...',
			aiConfidence: 'Confiance IA',
			sessionStats: 'Statistiques de session',
			ideasGenerated: 'Idées générées:',
			tagsCreated: 'Tags créés:',
			avgConfidence: 'Confiance moy.:',
			professionalSettings: 'Paramètres professionnels',
			aiBehavior: 'Comportement IA',
			tagCreationCount: 'Nombre de création de tags',
			ideaCount: 'Nombre d\'idées',
			confidenceThreshold: 'Seuil de confiance',
			suggestionCooldown: 'Délai de suggestion',
			features: 'Fonctionnalités',
			autoTagging: 'Auto-tagging',
			ideaFiltering: 'Filtrage d\'idées',
			appearance: 'Apparence',
			theme: 'Thème',
			sessionTags: 'Tags de session',
			activeTags: 'Tags actifs:',
			nextIdeas: 'Prochaines idées:',
			explore: 'Explorer',
			continueTalking: 'Cliquez pour continuer à parler de',
			clickToExplore: 'Cliquez pour explorer',
			debug: 'Debug',
			recording: 'Enregistrement',
			websocket: 'WebSocket',
			testMode: 'Mode test',
			on: 'Activé',
			off: 'Désactivé',
			connected: 'Connecté',
			disconnected: 'Déconnecté',
			yes: 'Oui',
			no: 'Non',
			yourThoughts: 'Vos Pensées'
		},
		tr: {
			appName: 'NextWord',
			ready: 'HAZIR',
			listening: 'DİNLİYOR',
			aiAnalyzing: 'AI konuşmanızı analiz ediyor...',
			waitingForSpeech: 'Konuşma bekleniyor...',
			audioControl: 'Ses Kontrolü',
			startRecording: 'Kaydı Başlat',
			stopRecording: 'Kaydı Durdur',
			audioLevel: 'Ses Seviyesi',
			liveTranscript: 'Canlı Transkript',
			current: 'Mevcut',
			fullSession: 'Tam Oturum',
			startSpeaking: 'Konuşmaya başlayın, kelimelerinizi burada görmek için...',
			aiSuggestions: 'AI Önerileri',
			aiSuggestionsPlaceholder: 'AI önerileri burada görünecek...',
			documentContext: 'Belge Bağlamı',
			uploadDocument: 'Belge Yükle',
			pasteText: 'Veya AI analizi için metninizi buraya yapıştırın...',
			analyzeText: 'Metni Analiz Et',
			documentPreview: 'Belge Bağlamı:',
			clear: 'Temizle',
			analyzingDocument: 'AI belgenizi analiz ediyor...',
			topicTags: 'Konu Etiketleri',
			topicTagsPlaceholder: 'Konu etiketleri burada görünecek...',
			aiConfidence: 'AI Güveni',
			sessionStats: 'Oturum İstatistikleri',
			ideasGenerated: 'Üretilen Fikirler:',
			tagsCreated: 'Oluşturulan Etiketler:',
			avgConfidence: 'Ort. Güven:',
			professionalSettings: 'Profesyonel Ayarlar',
			aiBehavior: 'AI Davranışı',
			tagCreationCount: 'Etiket Oluşturma Sayısı',
			ideaCount: 'Fikir Sayısı',
			confidenceThreshold: 'Güven Eşiği',
			suggestionCooldown: 'Öneri Bekleme Süresi',
			features: 'Özellikler',
			autoTagging: 'Otomatik Etiketleme',
			ideaFiltering: 'Fikir Filtreleme',
			appearance: 'Görünüm',
			theme: 'Tema',
			sessionTags: 'Oturum Etiketleri',
			activeTags: 'Aktif Etiketler:',
			nextIdeas: 'Sonraki Fikirler:',
			explore: 'Keşfet',
			continueTalking: 'Hakkında konuşmaya devam etmek için tıklayın',
			clickToExplore: 'Keşfetmek için tıklayın',
			debug: 'Hata Ayıklama',
			recording: 'Kayıt',
			websocket: 'WebSocket',
			testMode: 'Test Modu',
			on: 'Açık',
			off: 'Kapalı',
			connected: 'Bağlı',
			disconnected: 'Bağlantı Kesildi',
			yes: 'Evet',
			no: 'Hayır',
			yourThoughts: 'Düşünceleriniz'
		}
	};

	function t(key: string): string {
		// Simple translation function that works
		const lang = translations[currentLanguage as keyof typeof translations];
		if (lang && key in lang) {
			return (lang as any)[key];
		}
		return (translations.en as any)[key] || key;
	}
	
	// Mind map state
	let centerNode = { id: 'center', text: 'Your Thoughts', x: 400, y: 300 };
	let nodeId = 0;
	
	async function startRecording() {
		console.log('Start recording clicked');
		// Use browser speech recognition instead of audio recording
		startBrowserSpeechRecognition();
	}

	function stopRecording() {
		console.log('Stop recording clicked');
		// Stop browser speech recognition
		stopBrowserSpeechRecognition();
		isRecording = false;
		isListening = false;
		audioLevel = 0;
	}

	function addMindMapNode(text: string) {
		if (text.trim()) {
			// Extract idea from text (first few words or key concept)
			const idea = extractIdeaFromText(text);
			
			// Check if similar idea already exists
			const existingNode = mindMapNodes.find(node => 
				node.text.toLowerCase().includes(idea.toLowerCase()) || 
				idea.toLowerCase().includes(node.text.toLowerCase())
			);
			
			if (existingNode) {
				// Highlight existing node instead of creating new one
				highlightNode(existingNode.id);
				return;
			}
			
			const newNode = {
				id: `node-${nodeId++}`,
				text: idea,
				x: 400 + (Math.random() - 0.5) * 300,
				y: 300 + (Math.random() - 0.5) * 200,
				connections: [centerNode.id],
				highlighted: false
			};
			mindMapNodes = [...mindMapNodes, newNode];
		}
	}

	function extractIdeaFromText(text: string): string {
		// Extract key idea from text (first few meaningful words)
		const words = text.trim().split(' ');
		if (words.length <= 3) return text;
		
		// Look for key concepts - prioritize nouns and important words
		const importantWords = words.slice(0, 4).filter(word => 
			word.length > 2 && 
			!['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'].includes(word.toLowerCase())
		);
		
		if (importantWords.length >= 2) {
			return importantWords.slice(0, 3).join(' ');
		}
		
		// Fallback to first 3 words
		return words.slice(0, 3).join(' ');
	}

	function highlightNode(nodeId: string) {
		mindMapNodes = mindMapNodes.map(node => 
			node.id === nodeId 
				? { ...node, highlighted: true }
				: { ...node, highlighted: false }
		);
		
		// Remove highlight after 3 seconds
		setTimeout(() => {
			mindMapNodes = mindMapNodes.map(node => 
				node.id === nodeId 
					? { ...node, highlighted: false }
					: node
			);
		}, 3000);
	}

	function toggleSettings() {
		settingsOpen = !settingsOpen;
	}

	function toggleTags() {
		tagsOpen = !tagsOpen;
	}

	function toggleTag(tag: string) {
		if (selectedTags.includes(tag)) {
			selectedTags = selectedTags.filter(t => t !== tag);
		} else {
			selectedTags = [...selectedTags, tag];
		}
	}

	function switchTheme(theme: string) {
		currentTheme = theme;
	}

	function switchLanguage(language: string) {
		currentLanguage = language;
	}

	async function saveSpeechSettings() {
		try {
			const response = await fetch(`${BACKEND_URL}/settings`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(speechSettings)
			});
			
			if (response.ok) {
				console.log('Speech settings saved successfully');
			} else {
				console.error('Failed to save speech settings');
			}
		} catch (error) {
			console.error('Error saving speech settings:', error);
		}
	}

	// Browser Speech Recognition Functions
	function initSpeechRecognition() {
		console.log('Initializing speech recognition');
		if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
			const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
			recognition = new SpeechRecognition();
			console.log('Speech recognition created');
			
			recognition.continuous = true;
			recognition.interimResults = true;
			recognition.lang = speechSettings.language;
			
			recognition.onstart = () => {
				isListening = true;
				isRecording = true;
				console.log('Speech recognition started');
			};
			
			recognition.onresult = (event: any) => {
				let finalTranscript = '';
				let interimTranscript = '';
				
				for (let i = event.resultIndex; i < event.results.length; i++) {
					const transcript = event.results[i][0].transcript;
					if (event.results[i].isFinal) {
						finalTranscript += transcript;
					} else {
						interimTranscript += transcript;
					}
				}
				
				// Update the text area with both final and interim results
				speechText = finalTranscript + interimTranscript;
				
				// Update the main transcript display
				currentTranscript = finalTranscript + interimTranscript;
				if (finalTranscript.trim()) {
					fullTranscript += finalTranscript + ' ';
					// Add new node to mind map
					addMindMapNode(finalTranscript);
				}
				
				// Send final results to backend for AI analysis
				if (finalTranscript.trim()) {
					console.log('Sending final transcript to backend:', finalTranscript.trim());
					sendSpeechToBackend(finalTranscript.trim());
				}
			};
			
			recognition.onerror = (event: any) => {
				console.error('Speech recognition error:', event.error);
				isListening = false;
				isRecording = false;
			};
			
			recognition.onend = () => {
				isListening = false;
				isRecording = false;
				console.log('Speech recognition ended');
			};
		} else {
			console.error('Speech recognition not supported in this browser');
		}
	}

	async function startBrowserSpeechRecognition() {
		console.log('Starting browser speech recognition');
		
		// Start audio level monitoring
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ 
				audio: {
					sampleRate: 44100,
					channelCount: 1,
					echoCancellation: true,
					noiseSuppression: true,
					autoGainControl: true
				}
			});
			
			// Start real audio level monitoring
			startRealAudioLevelMonitoring(stream);
		} catch (error) {
			console.error('Error accessing microphone for audio level:', error);
		}
		
		if (recognition) {
			recognition.start();
		} else {
			initSpeechRecognition();
			if (recognition) {
				recognition.start();
			}
		}
		isRecording = true;
	}

	function stopBrowserSpeechRecognition() {
		console.log('Stopping browser speech recognition');
		if (recognition) {
			recognition.stop();
		}
		
		// Clean up audio monitoring
		if (audioLevelInterval) {
			clearInterval(audioLevelInterval);
			audioLevelInterval = null;
		}
		if (audioContext) {
			audioContext.close();
			audioContext = null;
			analyser = null;
		}
		
		isListening = false;
		isRecording = false;
		audioLevel = 0;
	}

	async function sendSpeechToBackend(text: string) {
		console.log('Sending speech to backend:', text);
		try {
			const response = await fetch(`${BACKEND_URL}/analyze-speech`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ text: text })
			});
			
			if (response.ok) {
				const result = await response.json();
				console.log('AI Analysis result:', result);
				
				// Update the UI with AI suggestions
				if (result.ideas && result.ideas.length > 0) {
					console.log('Adding ideas:', result.ideas);
					ideaSuggestions = [...ideaSuggestions, ...result.ideas];
					sessionStats.totalIdeas += result.ideas.length;
					// Keep only last N ideas based on settings
					if (ideaSuggestions.length > ideaCount) {
						ideaSuggestions = ideaSuggestions.slice(-ideaCount);
					}
				}
				if (result.tags && result.tags.length > 0) {
					console.log('Adding tags:', result.tags);
					aiTags = [...aiTags, ...result.tags];
					sessionStats.totalTags += result.tags.length;
					// Keep only last N tags based on settings
					if (aiTags.length > tagCreationCount) {
						aiTags = aiTags.slice(-tagCreationCount);
					}
					console.log('Updated aiTags array:', aiTags);
				}
				if (result.confidence) {
					confidenceLevel = result.confidence;
					// Update session stats
					sessionStats.confidenceAvg = (sessionStats.confidenceAvg + confidenceLevel) / 2;
				}
				
				// Stop listening when AI analysis is complete
				isListening = false;
			}
		} catch (error) {
			console.error('Error sending speech to backend:', error);
		}
	}

	function clearTranscript() {
		currentTranscript = '';
		fullTranscript = '';
		mindMapNodes = [];
		suggestions = [];
		ideaSuggestions = [];
		aiTags = [];
		confidenceLevel = 0;
		sessionStats = {
			totalIdeas: 0,
			totalTags: 0,
			confidenceAvg: 0,
			sessionTime: 0
		};
	}

	// Test function to manually trigger AI analysis
	async function testAI() {
		console.log('Testing AI analysis...');
		await sendSpeechToBackend('I want to focus on business strategy and marketing');
	}

	function toggleTestMode() {
		testMode = !testMode;
		if (testMode) {
			// Simulate some test data
			setTimeout(() => {
				currentTranscript = "This is a test of the transcript feature.";
				fullTranscript = "This is a test of the transcript feature. ";
				addMindMapNode("Test transcript");
			}, 1000);
		}
	}

	function clickTag(tag: string) {
		// Add the clicked tag as a new transcript to continue the conversation
		const tagTranscript = `Let me continue talking about ${tag}`;
		currentTranscript = tagTranscript;
		fullTranscript += tagTranscript + ' ';
		addMindMapNode(tagTranscript);
		
		// Trigger AI analysis for the new topic
		if (socket && socket.readyState === WebSocket.OPEN) {
			// Simulate sending audio data to trigger AI analysis
			socket.send(new Blob(['clicked-tag-trigger']));
		}
	}

	function clickIdea(idea: string) {
		// Add the clicked idea as a new transcript to continue the conversation
		const ideaTranscript = `I want to explore ${idea}`;
		currentTranscript = ideaTranscript;
		fullTranscript += ideaTranscript + ' ';
		addMindMapNode(ideaTranscript);
		
		// Trigger AI analysis for the new topic
		if (socket && socket.readyState === WebSocket.OPEN) {
			// Simulate sending audio data to trigger AI analysis
			socket.send(new Blob(['clicked-idea-trigger']));
		}
	}

	async function handleFileUpload(event: Event) {
		const target = event.target as HTMLInputElement;
		const file = target.files?.[0];
		if (!file) return;

		uploadedFile = file;
		isAnalyzingDocument = true;

		try {
			const text = await file.text();
			uploadedText = text;
			documentContext = text.substring(0, 1000); // First 1000 chars for context
			
			// Send document context to backend for analysis
			if (socket && socket.readyState === WebSocket.OPEN) {
				socket.send(JSON.stringify({
					type: 'document_analysis',
					content: text,
					filename: file.name
				}));
			}
		} catch (error) {
			console.error('Error reading file:', error);
		}
	}

	function handleTextInput() {
		if (uploadedText.trim()) {
			documentContext = uploadedText.substring(0, 1000);
			isAnalyzingDocument = true;
			
			// Send text context to backend for analysis
			if (socket && socket.readyState === WebSocket.OPEN) {
				socket.send(JSON.stringify({
					type: 'document_analysis',
					content: uploadedText,
					filename: 'user_input.txt'
				}));
			}
		}
	}

	function clearDocument() {
		uploadedFile = null;
		uploadedText = '';
		documentContext = '';
		isAnalyzingDocument = false;
	}

	// Real audio level monitoring
	let audioContext: AudioContext | null = null;
	let analyser: AnalyserNode | null = null;
	let audioLevelInterval: any = null;

	function calculateRealAudioLevel(stream: MediaStream) {
		if (!audioContext) {
			audioContext = new AudioContext();
			analyser = audioContext.createAnalyser();
			const source = audioContext.createMediaStreamSource(stream);
			source.connect(analyser);
			analyser.fftSize = 256;
		}
	}

	function startRealAudioLevelMonitoring(stream: MediaStream) {
		calculateRealAudioLevel(stream);
		
		audioLevelInterval = setInterval(() => {
			if (isRecording && analyser) {
				const dataArray = new Uint8Array(analyser.frequencyBinCount);
				analyser.getByteFrequencyData(dataArray);
				
				// Calculate average volume
				let sum = 0;
				for (let i = 0; i < dataArray.length; i++) {
					sum += dataArray[i];
				}
				const average = sum / dataArray.length;
				audioLevel = Math.min(100, (average / 128) * 100);
			} else {
				audioLevel = 0;
				if (audioLevelInterval) {
					clearInterval(audioLevelInterval);
					audioLevelInterval = null;
				}
			}
		}, 100);
	}
</script>

<div class="app-container" data-theme={currentTheme}>
	<!-- Header -->
	<header class="header">
		<div class="header-left">
			<div class="logo">
				<div class="logo-icon">NW</div>
				<span class="logo-text">{t('appName')}</span>
			</div>
		</div>
		
		<div class="header-center">
			<div class="recording-status" class:recording={isRecording}>
				<div class="status-indicator"></div>
				<span>{isRecording ? t('listening') : t('ready')}</span>
			</div>
			{#if isListening}
				<div class="listening-indicator">
					<div class="listening-dots">
						<div class="dot"></div>
						<div class="dot"></div>
						<div class="dot"></div>
					</div>
					<span>{t('aiAnalyzing')}</span>
				</div>
			{:else if isRecording && audioLevel < 5}
				<div class="waiting-indicator">
					<div class="waiting-icon">🎤</div>
					<span>{t('waitingForSpeech')}</span>
				</div>
			{/if}
		</div>
		
		<div class="header-right">
			<button class="icon-btn" on:click={toggleSettings} class:active={settingsOpen} title="Settings">
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
					<path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
				</svg>
			</button>
			<button class="icon-btn" on:click={toggleTags} class:active={tagsOpen} title="Tags">
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
					<path d="M5.5,7A1.5,1.5 0 0,1 4,5.5A1.5,1.5 0 0,1 5.5,4A1.5,1.5 0 0,1 7,5.5A1.5,1.5 0 0,1 5.5,7M21.41,11.58L12.41,2.58C12.05,2.22 11.55,2 11,2H4C2.89,2 2,2.89 2,4V11C2,11.55 2.22,12.05 2.59,12.41L11.58,21.41C11.95,21.77 12.45,22 13,22C13.55,22 14.05,21.77 14.41,21.41L21.41,14.41C21.77,14.05 22,13.55 22,13C22,12.45 21.77,11.95 21.41,11.58Z"/>
				</svg>
			</button>
			<button class="icon-btn" on:click={toggleTestMode} title="Test Mode" class:active={testMode}>
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
					<path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M11,16.5L18,9.5L16.5,8L11,13.5L7.5,10L6,11.5L11,16.5Z"/>
				</svg>
			</button>
			<button class="icon-btn" on:click={clearTranscript} title="Clear All">
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
					<path d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"/>
				</svg>
			</button>
			<button class="icon-btn" on:click={testAI} title="Test AI">
				<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
					<path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M11,16.5L18,9.5L16.5,8L11,13.5L7.5,10L6,11.5L11,16.5Z"/>
				</svg>
			</button>
		</div>
	</header>

	<!-- Main Content -->
	<main class="main-content">
		<!-- Left Panel - Controls -->
		<div class="left-panel">
			<div class="control-section">
				<h3>{t('audioControl')}</h3>
				<div class="recording-controls">
					<button 
						class="record-btn" 
						on:click={startRecording} 
						disabled={isRecording}
						class:recording={isRecording}
					>
						<svg class="btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
							<path d="M12,14C13.66,14 15,12.66 15,11V5C15,3.34 13.66,2 12,2C10.34,2 9,3.34 9,5V11C9,12.66 10.34,14 12,14M19,11C19,15.42 15.42,19 11,19H13V21H15V19H17V17H11C7.13,17 4,13.87 4,10H6C6,12.76 8.24,15 11,15H13V17H11C8.79,17 7,15.21 7,13H9C9,14.1 9.9,15 11,15H13V17H11C9.9,17 9,16.1 9,15H7C7,13.9 7.9,13 9,13H11V15H9C7.9,15 7,14.1 7,13H5C5,15.21 6.79,17 9,17H11V19H9C6.79,19 5,17.21 5,15H7C7,16.1 7.9,17 9,17H11V19H9C7.9,19 7,18.1 7,17H5C5,19.21 6.79,21 9,21H11V23H13V21H15V19H17V17H19V15H17V13H19V11Z"/>
						</svg>
						<span>{t('startRecording')}</span>
					</button>
					
					<button 
						class="stop-btn" 
						on:click={stopRecording} 
						disabled={!isRecording}
					>
						<svg class="btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
							<path d="M6,6H18V18H6V6Z"/>
						</svg>
						<span>{t('stopRecording')}</span>
					</button>
				</div>
				
				<!-- Audio Level Indicator -->
				{#if isRecording}
					<div class="audio-level">
						<div class="level-bar">
							<div class="level-fill" style="width: {audioLevel}%"></div>
						</div>
						<span>{t('audioLevel')}: {Math.round(audioLevel)}%</span>
					</div>
				{/if}
			</div>

			<div class="control-section">
				<h3>{t('liveTranscript')}</h3>
				<div class="transcript-box">
					{#if currentTranscript}
						<div class="current-transcript">
							<strong>{t('current')}:</strong> {currentTranscript}
						</div>
					{/if}
					{#if fullTranscript}
						<div class="full-transcript">
							<strong>{t('fullSession')}:</strong>
							<p>{fullTranscript}</p>
						</div>
					{:else}
						<p class="placeholder">{t('startSpeaking')}</p>
					{/if}
					
					<!-- Debug Info -->
					<div class="debug-info">
						<small>
							<strong>Debug:</strong><br>
							Recording: {isRecording ? 'Yes' : 'No'}<br>
							WebSocket: {socket ? ((socket as any).readyState === 1 ? 'Connected' : 'Disconnected') : 'Not connected'}<br>
							Audio Level: {Math.round(audioLevel)}% (Real: {audioContext ? 'Yes' : 'No'})<br>
							Speech Recognition: {socket ? 'Active' : 'Inactive'}<br>
							Test Mode: {testMode ? 'On' : 'Off'}
						</small>
					</div>
				</div>
			</div>


			<div class="control-section">
				<h3>{t('aiSuggestions')}</h3>
				<div class="suggestions-box">
					{#each ideaSuggestions as suggestion, index}
						<button class="suggestion-item clickable-suggestion" on:click={() => clickIdea(suggestion)} title="{t('clickToExplore')} {suggestion}">
							<span class="suggestion-text">{suggestion}</span>
							<span class="suggestion-action">{t('explore')} →</span>
						</button>
					{:else}
						<p class="placeholder">{t('aiSuggestionsPlaceholder')}</p>
		{/each}
</div>
			</div>

			<div class="control-section">
				<h3>Document Context</h3>
				<div class="document-upload">
					<div class="upload-area">
						<input 
							type="file" 
							id="file-upload" 
							accept=".txt,.md,.pdf,.doc,.docx" 
							on:change={handleFileUpload}
							style="display: none;"
						/>
						<label for="file-upload" class="upload-btn">
							<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
								<path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
							</svg>
							Upload Document
						</label>
					</div>
					
					<div class="text-input-area">
						<textarea 
							bind:value={uploadedText}
							placeholder="Or paste your text here for AI analysis..."
							class="text-input"
							rows="4"
						></textarea>
						<button class="analyze-btn" on:click={handleTextInput} disabled={!uploadedText.trim()}>
							Analyze Text
						</button>
					</div>
					
					{#if documentContext}
						<div class="document-preview">
							<h4>Document Context:</h4>
							<p class="context-text">{documentContext}...</p>
							<button class="clear-btn" on:click={clearDocument}>Clear</button>
						</div>
					{/if}
					
					{#if isAnalyzingDocument}
						<div class="analyzing-indicator">
							<div class="analyzing-dots">
								<div class="dot"></div>
								<div class="dot"></div>
								<div class="dot"></div>
							</div>
							<span>AI is analyzing your document...</span>
						</div>
					{/if}
				</div>
			</div>

			<div class="control-section">
				<h3>Topic Tags</h3>
				<div class="tags-box">
					{#each aiTags as tag, index}
						<button class="tag-item clickable-tag-item" on:click={() => clickTag(tag)} title="Click to continue talking about {tag}">
							{tag}
						</button>
					{:else}
						<p class="placeholder">Topic tags will appear here...</p>
					{/each}
				</div>
			</div>
		</div>

		<!-- Center - Mind Map with AI Tags -->
		<div class="mind-map-container">
			<!-- AI Tags Overlay - Large and Focused -->
			{#if aiTags.length > 0}
				<div class="ai-tags-overlay">
					{#each aiTags as tag, index}
						<button class="ai-tag-large clickable-tag" style="animation-delay: {index * 0.2}s" on:click={() => clickTag(tag)} title="Click to continue talking about {tag}">
							{tag}
						</button>
					{/each}
				</div>
			{/if}

			<!-- Idea Suggestions Overlay -->
			{#if ideaSuggestions.length > 0}
				<div class="ideas-overlay">
					<h3>Next Ideas:</h3>
					{#each ideaSuggestions as idea, index}
						<button class="idea-item clickable-idea" style="animation-delay: {index * 0.1}s" on:click={() => clickIdea(idea)} title="Click to explore {idea}">
							{idea}
						</button>
					{/each}
				</div>
			{/if}

			<svg class="mind-map" viewBox="0 0 800 600">
				<!-- Connections -->
				{#each mindMapNodes as node}
					<line 
						x1={centerNode.x} 
						y1={centerNode.y} 
						x2={node.x} 
						y2={node.y} 
						class="connection-line"
					/>
				{/each}
				
				<!-- Center Node -->
				<circle 
					cx={centerNode.x} 
					cy={centerNode.y} 
					r="30" 
					class="center-node"
				/>
				<text 
					x={centerNode.x} 
					y={centerNode.y + 5} 
					text-anchor="middle" 
					class="center-text"
				>
					{t('yourThoughts')}
				</text>
				
				<!-- Mind Map Nodes -->
				{#each mindMapNodes as node}
					<circle 
						cx={node.x} 
						cy={node.y} 
						r="20" 
						class="mind-node"
						class:highlighted={node.highlighted}
					/>
					<text 
						x={node.x} 
						y={node.y + 5} 
						text-anchor="middle" 
						class="node-text"
						class:highlighted={node.highlighted}
					>
						{node.text.length > 12 ? node.text.substring(0, 12) + '...' : node.text}
					</text>
				{/each}
			</svg>
		</div>

		<!-- Right Panel - Professional Tools & Settings -->
		<div class="right-panel">
			<!-- Confidence Gauge -->
			<div class="confidence-gauge">
				<h3>AI Confidence</h3>
				<div class="gauge-container">
					<div class="gauge-circle">
						<svg class="gauge-svg" viewBox="0 0 120 120">
							<circle cx="60" cy="60" r="50" fill="none" stroke="var(--secondary-color)" stroke-width="8"/>
							<circle cx="60" cy="60" r="50" fill="none" stroke="var(--accent-color)" stroke-width="8" 
								stroke-dasharray="{314 * confidenceLevel / 100}" 
								stroke-dashoffset="78.5" 
								transform="rotate(-90 60 60)"
								class="gauge-fill"/>
							<text x="60" y="65" text-anchor="middle" class="gauge-text">{confidenceLevel}%</text>
						</svg>
					</div>
				</div>
			</div>

			<!-- Session Statistics -->
			<div class="session-stats">
				<h3>Session Stats</h3>
				<div class="stat-item">
					<span class="stat-label">Ideas Generated:</span>
					<span class="stat-value">{sessionStats.totalIdeas}</span>
				</div>
				<div class="stat-item">
					<span class="stat-label">Tags Created:</span>
					<span class="stat-value">{sessionStats.totalTags}</span>
				</div>
				<div class="stat-item">
					<span class="stat-label">Avg Confidence:</span>
					<span class="stat-value">{Math.round(sessionStats.confidenceAvg)}%</span>
				</div>
			</div>

			{#if settingsOpen}
				<div class="settings-panel">
					<h3>Professional Settings</h3>
					
					<div class="setting-group">
						<h4>AI Behavior</h4>
						<div class="setting-item">
							<label for="tag-count">Tag Creation Count</label>
							<input id="tag-count" type="range" min="1" max="10" bind:value={tagCreationCount} />
							<span class="setting-value">{tagCreationCount}</span>
						</div>
						<div class="setting-item">
							<label for="idea-count">Idea Count</label>
							<input id="idea-count" type="range" min="3" max="15" bind:value={ideaCount} />
							<span class="setting-value">{ideaCount}</span>
						</div>
						<div class="setting-item">
							<label for="confidence-threshold">Confidence Threshold</label>
							<input id="confidence-threshold" type="range" min="50" max="95" bind:value={confidenceThreshold} />
							<span class="setting-value">{confidenceThreshold}%</span>
						</div>
						<div class="setting-item">
							<label for="suggestion-cooldown">Suggestion Cooldown</label>
							<input id="suggestion-cooldown" type="range" min="1" max="10" bind:value={suggestionCooldown} />
							<span class="setting-value">{suggestionCooldown}s</span>
						</div>
					</div>

					<div class="setting-group">
						<h4>Features</h4>
						<div class="setting-item">
							<label for="auto-tagging">Auto Tagging</label>
							<input id="auto-tagging" type="checkbox" bind:checked={autoTagging} />
						</div>
						<div class="setting-item">
							<label for="idea-filtering">Idea Filtering</label>
							<input id="idea-filtering" type="checkbox" bind:checked={ideaFiltering} />
						</div>
					</div>

					<div class="setting-group">
						<h4>{t('appearance')}</h4>
						<div class="setting-item">
							<label for="theme-select">{t('theme')}</label>
							<select id="theme-select" on:change={(e) => switchTheme((e.target as HTMLSelectElement).value)}>
								{#each Object.entries(themes) as [key, theme]}
									<option value={key} selected={currentTheme === key}>{theme.name}</option>
								{/each}
							</select>
						</div>
						<div class="setting-item">
							<label for="language-select">Language</label>
							<select id="language-select" on:change={(e) => switchLanguage((e.target as HTMLSelectElement).value)}>
								<option value="en" selected={currentLanguage === 'en'}>English</option>
								<option value="de" selected={currentLanguage === 'de'}>Deutsch</option>
								<option value="fr" selected={currentLanguage === 'fr'}>Français</option>
								<option value="tr" selected={currentLanguage === 'tr'}>Türkçe</option>
							</select>
						</div>
					</div>

					<div class="setting-group">
						<h4>{t('speechRecognition')}</h4>
						<div class="setting-item">
							<label for="speech-language">{t('language')}</label>
							<select id="speech-language" bind:value={speechSettings.language}>
								<option value="en-US">English (US)</option>
								<option value="en-GB">English (UK)</option>
								<option value="de-DE">German</option>
								<option value="fr-FR">French</option>
								<option value="tr-TR">Turkish</option>
								<option value="es-ES">Spanish</option>
								<option value="it-IT">Italian</option>
								<option value="pt-BR">Portuguese</option>
								<option value="ru-RU">Russian</option>
								<option value="ja-JP">Japanese</option>
								<option value="ko-KR">Korean</option>
								<option value="zh-CN">Chinese (Simplified)</option>
							</select>
						</div>
						<div class="setting-item">
							<label for="speech-confidence">{t('speechConfidence')}</label>
							<input id="speech-confidence" type="range" min="0.1" max="1.0" step="0.1" bind:value={speechSettings.confidenceThreshold} />
							<span class="setting-value">{Math.round(speechSettings.confidenceThreshold * 100)}%</span>
						</div>
						<div class="setting-item">
							<label for="use-google-cloud">{t('useGoogleCloud')}</label>
							<input id="use-google-cloud" type="checkbox" bind:checked={speechSettings.useGoogleCloud} />
						</div>
						<div class="setting-item">
							<label for="fallback-offline">{t('fallbackOffline')}</label>
							<input id="fallback-offline" type="checkbox" bind:checked={speechSettings.fallbackToOffline} />
						</div>
						<div class="setting-item">
							<label for="audio-format">{t('audioFormat')}</label>
							<select id="audio-format" bind:value={speechSettings.audioFormat}>
								<option value="webm">WebM</option>
								<option value="mp4">MP4</option>
								<option value="wav">WAV</option>
								<option value="ogg">OGG</option>
							</select>
						</div>
						<div class="setting-item">
							<label for="sample-rate">{t('sampleRate')}</label>
							<select id="sample-rate" bind:value={speechSettings.sampleRate}>
								<option value="8000">8 kHz</option>
								<option value="16000">16 kHz</option>
								<option value="22050">22.05 kHz</option>
								<option value="44100">44.1 kHz</option>
								<option value="48000">48 kHz</option>
							</select>
						</div>
						<div class="setting-item">
							<label for="channels">{t('channels')}</label>
							<select id="channels" bind:value={speechSettings.channels}>
								<option value="1">Mono</option>
								<option value="2">Stereo</option>
							</select>
						</div>
						<div class="setting-item">
							<button class="save-settings-btn" on:click={saveSpeechSettings}>
								Save Speech Settings
							</button>
						</div>
					</div>
				</div>
			{/if}

			{#if tagsOpen}
				<div class="tags-panel">
					<h3>Session Tags</h3>
					<div class="tag-list">
						{#each availableTags as tag}
							<button 
								class="tag-btn" 
								on:click={() => toggleTag(tag)}
								class:selected={selectedTags.includes(tag)}
							>
								{tag}
							</button>
						{/each}
					</div>
					<div class="selected-tags">
						<h4>Active Tags:</h4>
						{#each selectedTags as tag}
							<span class="active-tag">{tag}</span>
						{/each}
					</div>
				</div>
			{/if}
		</div>
	</main>
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		background: #0a0a0a;
		color: #00ff00;
		font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		overflow: hidden;
		font-weight: 400;
		line-height: 1.5;
	}

	.app-container {
		height: 100vh;
		display: flex;
		flex-direction: column;
		background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
		transition: all 0.3s ease;
		--bg-color: #0a0a0a;
		--text-color: #00ff00;
		--accent-color: #00ff00;
		--secondary-color: #333;
	}

	/* Dynamic Theme Support */
	.app-container[data-theme="dark"] {
		--bg-color: #0a0a0a;
		--text-color: #00ff00;
		--accent-color: #00ff00;
		--secondary-color: #333;
		background: linear-gradient(135deg, var(--bg-color) 0%, #1a1a1a 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="light"] {
		--bg-color: #ffffff;
		--text-color: #000000;
		--accent-color: #0066cc;
		--secondary-color: #f0f0f0;
		background: linear-gradient(135deg, var(--bg-color) 0%, #f8f9fa 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="cyber"] {
		--bg-color: #000011;
		--text-color: #00ffff;
		--accent-color: #ff00ff;
		--secondary-color: #001122;
		background: linear-gradient(135deg, var(--bg-color) 0%, #001122 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="neon"] {
		--bg-color: #0d1117;
		--text-color: #39ff14;
		--accent-color: #ff0080;
		--secondary-color: #161b22;
		background: linear-gradient(135deg, var(--bg-color) 0%, #161b22 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="solar"] {
		--bg-color: #1a1a2e;
		--text-color: #ffd700;
		--accent-color: #ff6b35;
		--secondary-color: #16213e;
		background: linear-gradient(135deg, var(--bg-color) 0%, #16213e 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="ocean"] {
		--bg-color: #001122;
		--text-color: #00d4ff;
		--accent-color: #00ff88;
		--secondary-color: #002244;
		background: linear-gradient(135deg, var(--bg-color) 0%, #002244 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="forest"] {
		--bg-color: #0d1b0d;
		--text-color: #00ff41;
		--accent-color: #ffaa00;
		--secondary-color: #1a2e1a;
		background: linear-gradient(135deg, var(--bg-color) 0%, #1a2e1a 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="cosmic"] {
		--bg-color: #0f0f23;
		--text-color: #e94560;
		--accent-color: #f5a623;
		--secondary-color: #1a1a3a;
		background: linear-gradient(135deg, var(--bg-color) 0%, #1a1a3a 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="steel"] {
		--bg-color: #1e1e1e;
		--text-color: #c0c0c0;
		--accent-color: #ff4444;
		--secondary-color: #2d2d2d;
		background: linear-gradient(135deg, var(--bg-color) 0%, #2d2d2d 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="aurora"] {
		--bg-color: #0a0a0f;
		--text-color: #00ffcc;
		--accent-color: #ff3366;
		--secondary-color: #1a1a2e;
		background: linear-gradient(135deg, var(--bg-color) 0%, #1a1a2e 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="midnight"] {
		--bg-color: #000000;
		--text-color: #ffffff;
		--accent-color: #ff0080;
		--secondary-color: #1a1a1a;
		background: linear-gradient(135deg, var(--bg-color) 0%, #1a1a1a 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="sunset"] {
		--bg-color: #2d1b69;
		--text-color: #ff6b6b;
		--accent-color: #4ecdc4;
		--secondary-color: #3d2a7a;
		background: linear-gradient(135deg, var(--bg-color) 0%, #3d2a7a 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="emerald"] {
		--bg-color: #0d2818;
		--text-color: #00ff88;
		--accent-color: #ffd700;
		--secondary-color: #1a3d2a;
		background: linear-gradient(135deg, var(--bg-color) 0%, #1a3d2a 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="volcanic"] {
		--bg-color: #1a0d0d;
		--text-color: #ff4444;
		--accent-color: #ffaa00;
		--secondary-color: #2d1a1a;
		background: linear-gradient(135deg, var(--bg-color) 0%, #2d1a1a 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="arctic"] {
		--bg-color: #f0f8ff;
		--text-color: #0066cc;
		--accent-color: #00aaff;
		--secondary-color: #e6f3ff;
		background: linear-gradient(135deg, var(--bg-color) 0%, #e6f3ff 100%);
		color: var(--text-color);
	}

	.app-container[data-theme="lavender"] {
		--bg-color: #2d1b69;
		--text-color: #e6e6fa;
		--accent-color: #ff69b4;
		--secondary-color: #3d2a7a;
		background: linear-gradient(135deg, var(--bg-color) 0%, #3d2a7a 100%);
		color: var(--text-color);
	}

	/* Header */
	.header {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 100;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem 1rem;
		background: rgba(0, 0, 0, 0.9);
		border-bottom: 2px solid var(--accent-color);
		backdrop-filter: blur(10px);
		height: 60px;
	}

	.logo {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.logo-icon {
		width: 40px;
		height: 40px;
		background: var(--accent-color);
		color: var(--bg-color);
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: bold;
		border-radius: 4px;
	}

	.logo-text {
		font-size: 1.5rem;
		font-weight: bold;
		text-shadow: 0 0 10px var(--accent-color);
	}

	.recording-status {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		background: rgba(0, 0, 0, 0.5);
		border: 1px solid #333;
		border-radius: 4px;
	}

	.status-indicator {
		width: 12px;
		height: 12px;
		background: #666;
		border-radius: 50%;
		transition: all 0.3s ease;
	}

	.recording-status.recording .status-indicator {
		background: #ff0000;
		box-shadow: 0 0 10px #ff0000;
		animation: pulse 1s infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.5; }
	}

	/* Listening Indicator */
	.listening-indicator {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-top: 0.5rem;
		padding: 0.5rem 1rem;
		background: rgba(0, 255, 0, 0.1);
		border: 1px solid var(--accent-color);
		border-radius: 4px;
		animation: listening-glow 2s ease-in-out infinite;
	}

	.listening-dots {
		display: flex;
		gap: 4px;
	}

	.dot {
		width: 8px;
		height: 8px;
		background: var(--accent-color);
		border-radius: 50%;
		animation: dot-bounce 1.4s ease-in-out infinite both;
	}

	.dot:nth-child(1) { animation-delay: -0.32s; }
	.dot:nth-child(2) { animation-delay: -0.16s; }
	.dot:nth-child(3) { animation-delay: 0s; }

	@keyframes dot-bounce {
		0%, 80%, 100% {
			transform: scale(0);
		}
		40% {
			transform: scale(1);
		}
	}

	@keyframes listening-glow {
		0%, 100% {
			box-shadow: 0 0 5px var(--accent-color);
		}
		50% {
			box-shadow: 0 0 15px var(--accent-color);
		}
	}

	/* Waiting Indicator */
	.waiting-indicator {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-top: 0.5rem;
		padding: 0.5rem 1rem;
		background: rgba(255, 255, 0, 0.1);
		border: 1px solid #ffaa00;
		border-radius: 4px;
		animation: waiting-pulse 2s ease-in-out infinite;
	}

	.waiting-icon {
		font-size: 1.2rem;
		animation: waiting-bounce 1s ease-in-out infinite;
	}

	@keyframes waiting-pulse {
		0%, 100% {
			box-shadow: 0 0 5px #ffaa00;
		}
		50% {
			box-shadow: 0 0 15px #ffaa00;
		}
	}

	@keyframes waiting-bounce {
		0%, 100% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.1);
		}
	}

	.icon-btn {
		background: transparent;
		border: 1px solid var(--secondary-color);
		color: var(--text-color);
		padding: 0.5rem;
		border-radius: 4px;
		cursor: pointer;
		transition: all 0.3s ease;
	}

	.icon-btn:hover, .icon-btn.active {
		background: var(--accent-color);
		color: var(--bg-color);
		box-shadow: 0 0 10px var(--accent-color);
	}

	/* Main Content */
	.main-content {
		flex: 1;
		display: flex;
		height: calc(100vh - 60px);
		margin-top: 60px;
	}

	.left-panel, .right-panel {
		width: 250px;
		background: rgba(0, 0, 0, 0.6);
		border: 1px solid var(--secondary-color);
		padding: 0.5rem;
		overflow-y: auto;
	}

	.left-panel {
		border-right: 2px solid var(--accent-color);
	}

	.right-panel {
		border-left: 2px solid var(--accent-color);
	}

	.control-section {
		margin-bottom: 1rem;
	}

	.control-section h3 {
		color: var(--accent-color);
		margin-bottom: 0.5rem;
		text-shadow: 0 0 5px var(--accent-color);
		border-bottom: 1px solid var(--secondary-color);
		padding-bottom: 0.25rem;
		font-size: 0.9rem;
	}

	.recording-controls {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.record-btn, .stop-btn {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem;
		background: transparent;
		border: 2px solid var(--secondary-color);
		color: var(--text-color);
		cursor: pointer;
		transition: all 0.3s ease;
		border-radius: 4px;
		font-size: 0.8rem;
	}

	.record-btn:hover:not(:disabled) {
		border-color: var(--accent-color);
		box-shadow: 0 0 15px var(--accent-color);
	}

	.record-btn.recording {
		background: #ff0000;
		border-color: #ff0000;
		color: #fff;
		animation: pulse 1s infinite;
	}

	.stop-btn:hover:not(:disabled) {
		border-color: #ff0000;
		box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
	}

	.btn-icon {
		font-size: 1.2rem;
	}

	.audio-level {
		margin-top: 1rem;
	}

	.level-bar {
		width: 100%;
		height: 8px;
		background: #333;
		border-radius: 4px;
		overflow: hidden;
		margin-bottom: 0.5rem;
	}

	.level-fill {
		height: 100%;
		background: linear-gradient(90deg, #00ff00, #ffff00, #ff0000);
		transition: width 0.1s ease;
	}

	.transcript-box, .suggestions-box {
		background: rgba(0, 0, 0, 0.7);
		border: 2px solid var(--accent-color);
		border-radius: 8px;
		padding: 0.5rem;
		min-height: 80px;
		max-height: 120px;
		overflow-y: auto;
		box-shadow: 0 0 10px var(--accent-color);
	}

	.current-transcript {
		background: rgba(0, 255, 0, 0.1);
		border: 1px solid var(--accent-color);
		border-radius: 4px;
		padding: 0.5rem;
		margin-bottom: 0.5rem;
		font-weight: 500;
		animation: pulse-glow 2s ease-in-out infinite;
	}

	.full-transcript {
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid var(--secondary-color);
		border-radius: 4px;
		padding: 0.5rem;
		font-size: 0.9rem;
		line-height: 1.4;
	}

	@keyframes pulse-glow {
		0%, 100% { box-shadow: 0 0 5px var(--accent-color); }
		50% { box-shadow: 0 0 15px var(--accent-color); }
	}

	.debug-info {
		margin-top: 1rem;
		padding: 0.5rem;
		background: rgba(0, 0, 0, 0.5);
		border: 1px solid var(--secondary-color);
		border-radius: 4px;
		font-size: 0.8rem;
		color: var(--secondary-color);
	}

	.placeholder {
		color: #666;
		font-style: italic;
	}

	.suggestion-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem;
		background: rgba(0, 255, 0, 0.15);
		border: 2px solid var(--accent-color);
		border-radius: 6px;
		margin-bottom: 0.5rem;
		box-shadow: 0 0 8px var(--accent-color);
		transition: all 0.3s ease;
		width: 100%;
		text-align: left;
		font-size: 0.8rem;
	}

	.suggestion-item:hover {
		background: rgba(0, 255, 0, 0.25);
		box-shadow: 0 0 12px var(--accent-color);
		transform: translateY(-2px);
	}

	.clickable-suggestion {
		cursor: pointer;
		background: transparent;
		border: none;
		color: var(--text-color);
	}

	.suggestion-action {
		color: var(--accent-color);
		font-size: 0.8rem;
		font-weight: bold;
	}

	.tags-box {
		background: rgba(0, 0, 0, 0.7);
		border: 2px solid var(--accent-color);
		border-radius: 8px;
		padding: 0.5rem;
		min-height: 80px;
		max-height: 120px;
		overflow-y: auto;
		box-shadow: 0 0 10px var(--accent-color);
	}

	.tag-item {
		background: var(--accent-color);
		color: var(--bg-color);
		padding: 0.25rem 0.5rem;
		margin: 0.125rem;
		border-radius: 15px;
		font-size: 0.7rem;
		font-weight: 500;
		display: inline-block;
		cursor: pointer;
		transition: all 0.3s ease;
		border: none;
		box-shadow: 0 0 8px var(--accent-color);
	}

	.tag-item:hover {
		transform: translateY(-2px) scale(1.05);
		box-shadow: 0 0 15px var(--accent-color);
	}

	.clickable-tag-item:active {
		transform: translateY(0) scale(0.95);
	}

	/* Document Upload Styles */
	.document-upload {
		background: rgba(0, 0, 0, 0.7);
		border: 2px solid var(--accent-color);
		border-radius: 6px;
		padding: 0.4rem;
		box-shadow: 0 0 10px var(--accent-color);
		box-sizing: border-box;
	}

	.upload-area {
		margin-bottom: 0.5rem;
	}

	.upload-btn {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.4rem 0.6rem;
		background: var(--accent-color);
		color: var(--bg-color);
		border: none;
		border-radius: 4px;
		cursor: pointer;
		transition: all 0.3s ease;
		font-size: 0.75rem;
		font-weight: 500;
		width: 100%;
		justify-content: center;
		box-sizing: border-box;
	}

	.upload-btn:hover {
		background: var(--text-color);
		transform: translateY(-2px);
		box-shadow: 0 0 15px var(--accent-color);
	}

	.text-input-area {
		margin-bottom: 0.5rem;
	}

	.text-input {
		width: 100%;
		background: var(--secondary-color);
		border: 1px solid var(--accent-color);
		color: var(--text-color);
		padding: 0.4rem;
		border-radius: 4px;
		resize: vertical;
		font-family: inherit;
		font-size: 0.75rem;
		margin-bottom: 0.4rem;
		height: 50px;
		box-sizing: border-box;
	}

	.text-input:focus {
		outline: none;
		border-color: var(--accent-color);
		box-shadow: 0 0 10px var(--accent-color);
	}

	.analyze-btn {
		background: var(--accent-color);
		color: var(--bg-color);
		border: none;
		padding: 0.4rem 0.6rem;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.75rem;
		transition: all 0.3s ease;
		width: 100%;
		box-sizing: border-box;
	}

	.analyze-btn:hover:not(:disabled) {
		background: var(--text-color);
		transform: translateY(-1px);
		box-shadow: 0 0 10px var(--accent-color);
	}

	.analyze-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.document-preview {
		background: rgba(0, 0, 0, 0.5);
		border: 1px solid var(--secondary-color);
		border-radius: 6px;
		padding: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.document-preview h4 {
		color: var(--accent-color);
		margin: 0 0 0.25rem 0;
		font-size: 0.8rem;
	}

	.context-text {
		color: var(--text-color);
		font-size: 0.7rem;
		line-height: 1.3;
		margin: 0 0 0.25rem 0;
		opacity: 0.8;
		max-height: 40px;
		overflow: hidden;
	}

	.clear-btn {
		background: transparent;
		color: var(--accent-color);
		border: 1px solid var(--accent-color);
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.7rem;
		transition: all 0.3s ease;
	}

	.clear-btn:hover {
		background: var(--accent-color);
		color: var(--bg-color);
	}

	.analyzing-indicator {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem;
		background: rgba(0, 255, 0, 0.1);
		border: 1px solid var(--accent-color);
		border-radius: 4px;
		animation: analyzing-glow 2s ease-in-out infinite;
	}

	.analyzing-dots {
		display: flex;
		gap: 4px;
	}

	.analyzing-dots .dot {
		width: 6px;
		height: 6px;
		background: var(--accent-color);
		border-radius: 50%;
		animation: analyzing-bounce 1.4s ease-in-out infinite both;
	}

	.analyzing-dots .dot:nth-child(1) { animation-delay: -0.32s; }
	.analyzing-dots .dot:nth-child(2) { animation-delay: -0.16s; }
	.analyzing-dots .dot:nth-child(3) { animation-delay: 0s; }

	@keyframes analyzing-bounce {
		0%, 80%, 100% {
			transform: scale(0);
		}
		40% {
			transform: scale(1);
		}
	}

	@keyframes analyzing-glow {
		0%, 100% {
			box-shadow: 0 0 5px var(--accent-color);
		}
		50% {
			box-shadow: 0 0 15px var(--accent-color);
		}
	}

	/* Mind Map */
	.mind-map-container {
		flex: 1;
		background: radial-gradient(circle at center, rgba(0, 255, 0, 0.05) 0%, transparent 70%);
		position: relative;
		overflow: hidden;
	}

	/* AI Tags Overlay - Large and Focused */
	.ai-tags-overlay {
		position: absolute;
		top: 20px;
		left: 20px;
		right: 20px;
		z-index: 10;
		display: flex;
		flex-wrap: wrap;
		gap: 15px;
		justify-content: center;
	}

	.ai-tag-large {
		background: var(--accent-color);
		color: var(--bg-color);
		padding: 15px 25px;
		border-radius: 25px;
		font-size: 1.2rem;
		font-weight: bold;
		text-align: center;
		box-shadow: 0 0 20px var(--accent-color);
		animation: tag-pulse 2s ease-in-out infinite;
		transform: scale(1);
		transition: all 0.3s ease;
		min-width: 150px;
	}

	.ai-tag-large:hover {
		transform: scale(1.1);
		box-shadow: 0 0 30px var(--accent-color);
	}

	.clickable-tag {
		cursor: pointer;
		transition: all 0.3s ease;
	}

	.clickable-tag:hover {
		transform: scale(1.05);
		box-shadow: 0 0 25px var(--accent-color);
	}

	.clickable-tag:active {
		transform: scale(0.95);
	}

	@keyframes tag-pulse {
		0%, 100% { 
			transform: scale(1);
			box-shadow: 0 0 20px var(--accent-color);
		}
		50% { 
			transform: scale(1.05);
			box-shadow: 0 0 30px var(--accent-color);
		}
	}

	/* Idea Suggestions Overlay */
	.ideas-overlay {
		position: absolute;
		bottom: 20px;
		left: 20px;
		right: 20px;
		z-index: 10;
		background: rgba(0, 0, 0, 0.8);
		border: 2px solid var(--accent-color);
		border-radius: 15px;
		padding: 20px;
		backdrop-filter: blur(10px);
	}

	.ideas-overlay h3 {
		color: var(--accent-color);
		margin: 0 0 15px 0;
		text-align: center;
		font-size: 1.1rem;
		text-shadow: 0 0 10px var(--accent-color);
	}

	.idea-item {
		background: var(--accent-color);
		color: var(--bg-color);
		padding: 12px 18px;
		margin: 8px;
		border-radius: 25px;
		font-size: 0.9rem;
		font-weight: 500;
		display: inline-block;
		animation: idea-slide 0.5s ease-out;
		box-shadow: 0 0 15px var(--accent-color);
		transition: all 0.3s ease;
		max-width: 200px;
		text-align: center;
	}

	.idea-item:hover {
		transform: translateY(-3px) scale(1.05);
		box-shadow: 0 0 25px var(--accent-color);
	}

	.clickable-idea {
		cursor: pointer;
		transition: all 0.3s ease;
	}

	.clickable-idea:hover {
		transform: translateY(-3px) scale(1.05);
		box-shadow: 0 0 25px var(--accent-color);
	}

	.clickable-idea:active {
		transform: translateY(-1px) scale(1.02);
	}

	@keyframes idea-slide {
		from {
			opacity: 0;
			transform: translateY(20px) scale(0.9);
		}
		to {
			opacity: 1;
			transform: translateY(0) scale(1);
		}
	}

	/* Professional Tools */
	.confidence-gauge {
		background: rgba(0, 0, 0, 0.6);
		border: 1px solid var(--secondary-color);
		border-radius: 8px;
		padding: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.confidence-gauge h3 {
		color: var(--accent-color);
		margin: 0 0 0.5rem 0;
		text-align: center;
		font-size: 0.8rem;
	}

	.gauge-container {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.gauge-circle {
		width: 80px;
		height: 80px;
	}

	.gauge-svg {
		width: 100%;
		height: 100%;
		transform: rotate(0deg);
	}

	.gauge-fill {
		transition: stroke-dasharray 0.5s ease;
		stroke-linecap: round;
	}

	.gauge-text {
		fill: var(--text-color);
		font-size: 14px;
		font-weight: bold;
	}

	.session-stats {
		background: rgba(0, 0, 0, 0.6);
		border: 1px solid var(--secondary-color);
		border-radius: 8px;
		padding: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.session-stats h3 {
		color: var(--accent-color);
		margin: 0 0 0.5rem 0;
		text-align: center;
		font-size: 0.8rem;
	}

	.stat-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.25rem 0;
		border-bottom: 1px solid var(--secondary-color);
		font-size: 0.8rem;
	}

	.stat-item:last-child {
		border-bottom: none;
	}

	.stat-label {
		color: var(--text-color);
		font-size: 0.7rem;
	}

	.stat-value {
		color: var(--accent-color);
		font-weight: bold;
		font-size: 0.8rem;
	}

	.setting-group {
		margin-bottom: 0.5rem;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid var(--secondary-color);
	}

	.setting-group:last-child {
		border-bottom: none;
	}

	.setting-group h4 {
		color: var(--accent-color);
		margin: 0 0 0.5rem 0;
		font-size: 0.7rem;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.setting-value {
		color: var(--accent-color);
		font-weight: bold;
		margin-left: 0.5rem;
		min-width: 30px;
		text-align: right;
	}

	.mind-map {
		width: 100%;
		height: 100%;
	}

	.mind-node {
		fill: var(--secondary-color);
		stroke: var(--accent-color);
		stroke-width: 2;
		transition: all 0.3s ease;
	}

	.mind-node.highlighted {
		fill: var(--accent-color);
		stroke: var(--text-color);
		stroke-width: 3;
		animation: node-pulse 1s ease-in-out infinite;
	}

	.node-text {
		fill: var(--text-color);
		font-size: 10px;
		font-weight: 500;
		transition: all 0.3s ease;
	}

	.node-text.highlighted {
		fill: var(--bg-color);
		font-weight: bold;
		font-size: 11px;
	}

	@keyframes node-pulse {
		0%, 100% {
			opacity: 1;
			transform: scale(1);
		}
		50% {
			opacity: 0.8;
			transform: scale(1.1);
		}
	}

	.connection-line {
		stroke: var(--accent-color);
		stroke-width: 2;
		opacity: 0.6;
		animation: glow 2s ease-in-out infinite alternate;
	}

	@keyframes glow {
		from { opacity: 0.3; }
		to { opacity: 0.8; }
	}

	.center-node {
		fill: var(--accent-color);
		stroke: var(--bg-color);
		stroke-width: 3;
		filter: drop-shadow(0 0 10px var(--accent-color));
	}

	.center-text {
		fill: var(--bg-color);
		font-weight: bold;
		font-size: 12px;
	}

	.mind-node {
		fill: var(--secondary-color);
		stroke: var(--accent-color);
		stroke-width: 2;
		transition: all 0.3s ease;
	}

	.mind-node:hover {
		fill: var(--accent-color);
		filter: drop-shadow(0 0 5px var(--accent-color));
	}

	.node-text {
		fill: var(--accent-color);
		font-size: 10px;
		text-anchor: middle;
	}

	/* Settings & Tags Panels */
	.settings-panel, .tags-panel {
		background: rgba(0, 0, 0, 0.8);
		border: 1px solid var(--secondary-color);
		border-radius: 4px;
		padding: 1rem;
		margin-bottom: 1rem;
	}

	.setting-item {
		margin-bottom: 1rem;
	}

	.setting-item label {
		display: block;
		margin-bottom: 0.5rem;
		color: var(--accent-color);
	}

	.setting-item input, .setting-item select {
		width: 100%;
		background: var(--secondary-color);
		border: 1px solid var(--accent-color);
		color: var(--text-color);
		padding: 0.5rem;
		border-radius: 4px;
	}

	.tag-list {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	.tag-btn {
		background: transparent;
		border: 1px solid var(--secondary-color);
		color: var(--text-color);
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		cursor: pointer;
		transition: all 0.3s ease;
		font-size: 0.8rem;
	}

	.tag-btn:hover, .tag-btn.selected {
		background: var(--accent-color);
		color: var(--bg-color);
		box-shadow: 0 0 5px var(--accent-color);
	}

	.active-tag {
		display: inline-block;
		background: var(--accent-color);
		color: var(--bg-color);
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		margin: 0.25rem;
		font-size: 0.8rem;
	}

	/* Scrollbar Styling */
	::-webkit-scrollbar {
		width: 8px;
	}

	::-webkit-scrollbar-track {
		background: var(--secondary-color);
	}

	::-webkit-scrollbar-thumb {
		background: var(--accent-color);
		border-radius: 4px;
	}

	::-webkit-scrollbar-thumb:hover {
		background: var(--accent-color);
		opacity: 0.8;
	}

</style>