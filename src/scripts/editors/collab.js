import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';
import getDefaultSnippets from '../../constants/editorDefaultSnippets';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import { MonacoBinding } from 'y-monaco';

// setting up the editor
self.MonacoEnvironment = {
	getWorkerUrl: function (_, label) {
		if (label === 'typescript' || label === 'javascript') {
			return document.getElementById('typescript').value;
		}
		return document.getElementById('editor-worker').value;
	}
};

let editor = document.getElementById('editor');
editor.innerHTML = "";

editor = monaco.editor.create(editor, {
	value: getDefaultSnippets("javascript"),
	language: "javascript",
	theme: "vs-light",
	fontSize: 12
});

const evalBtn = document.getElementById('eval');
const themeSelect = document.getElementById('theme-select');
const fontSizeSelect = document.getElementById('font-size-select');
const editorId = document.getElementById("editor-id").value;
const resultArea = document.getElementById("result");
const languageSelect = document.getElementById('language-select');
const otherUser = document.getElementById('other-user-name')

themeSelect.addEventListener('change', (event) => {
	const theme = event.target.value;
	monaco.editor.setTheme(theme);
});

fontSizeSelect.addEventListener('change', (event) => {
	const fontSize = parseInt(event.target.value, 10);
	editor.updateOptions({ fontSize: fontSize });
});

function debounce(func, delay) {
	let timeout;
	return (...args) => {
		clearTimeout(timeout);
		timeout = setTimeout(() => func(...args), delay);
	};
}

// setting collab
const ydoc = new Y.Doc();
const provider = new WebsocketProvider('/ws/editor/collab/',`${editorId}/`, ydoc);
const awareness = provider.awareness
const yText = ydoc.getText();
new MonacoBinding(yText, editor.getModel(), new Set([editor]), awareness);

const debouncedSetCursorAwareness = debounce((position) => {
	awareness.setLocalStateField('cursor', {
		position,
		clientID: awareness.clientID
	});
}, 200);

editor.onDidChangeCursorSelection(_ => {
	const position = editor.getPosition();
	debouncedSetCursorAwareness(position);
})

// syncing up the language with the other side while initializing
const currentLanguage = awareness.getLocalState()?.selectedLanguage || 'javascript';
monaco.editor.setModelLanguage(editor.getModel(), currentLanguage);
languageSelect.value = currentLanguage;

let lastLocalUpdate = Date.now();
const debouncedSelectChange = debounce((selectedLanguage) => {
	awareness.setLocalStateField('language', {
		selectedLanguage,
		clientID: awareness.clientID,
		timestamp: lastLocalUpdate
	});
}, 200);

languageSelect.addEventListener('change', (e) => {
	lastLocalUpdate = Date.now();
	const selectedLanguage = e.target.value;
	monaco.editor.setModelLanguage(editor.getModel(), selectedLanguage);
	editor.setValue(getDefaultSnippets(languageSelect.value));
	debouncedSelectChange(selectedLanguage);
});

const remoteCursors = editor.createDecorationsCollection([]);
awareness.on('change', _ => {
	awareness.getStates().forEach((state, clientID) => {
		if (clientID !== awareness.clientID) {
			const cursor = state.cursor;
			if (cursor) {
				const decorations = [];
				const { position } = cursor;

				decorations.push({
					range: new monaco.Range(position.lineNumber, position.column, position.lineNumber, position.column),
					options: {
						className: 'remote-cursor',
						after: {
							content: '⟵ ' + otherUser.value,
							inlineClassName: 'remote-cursor-label'
						}
					}
				});

				remoteCursors.set(decorations);
			}
			const languageState = state.language;
			if (languageState && languageState.timestamp > lastLocalUpdate) {
				const { selectedLanguage } = languageState;
				monaco.editor.setModelLanguage(editor.getModel(), selectedLanguage);
				languageSelect.value = selectedLanguage;
			}
		}
	})
});

const connectWebsocket = () => {
	const resultWebSocket = new WebSocket(`/ws/editor/result/${editorId}/`)

	resultWebSocket.onopen = _ => {
		resultArea.innerText = "Happy Coding!";
	}

	evalBtn.addEventListener('click', () => {
		const code = editor.getValue().trim();
		if (code === "") {
			resultArea.innerText = "請先輸入程式代碼";
		} else {
			const params = {
				code: code,
				language: languageSelect.value
			}
			resultWebSocket.send(JSON.stringify(params));
			resultArea.innerText = "執行程式中......";
		}
	})

	resultWebSocket.onmessage = event => {
		resultArea.innerText = JSON.parse(event.data);
	};

	resultWebSocket.onclose = _ => {
		resultArea.innerText = "目前連線中斷中，請稍後";
		setTimeout(() => {
			connectWebsocket()
		}, 5000)
	}

	resultWebSocket.onerror = _ => {
		resultWebSocket.close();
	}
}

connectWebsocket();

