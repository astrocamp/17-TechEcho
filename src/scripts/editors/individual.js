import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';
import getDefaultSnippets from '../../constants/editorDefaultSnippets';
import Cookies from 'js-cookie';

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
const resultArea = document.getElementById("result");
const languageSelect = document.getElementById('language-select');

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

// individual editor
languageSelect.addEventListener('change', (event) => {
    const currentLanguage = event.target.value;
    editor.setValue(getDefaultSnippets(currentLanguage))
    monaco.editor.setModelLanguage(editor.getModel(), currentLanguage);
});

const evalCode = async () => {
    const code = editor.getValue().trim();
    if (code === "") {
        resultArea.innerText = "請先輸入程式代碼";
        return
    }
    resultArea.innerText = "執行程式中......";

    const params = new URLSearchParams();
    params.append('code', code);
    params.append('language', languageSelect.value);
    try {
        const response = await fetch(document.getElementById('eval-url').value, {
            method: 'POST',
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: params.toString(),
        })

        const data = await response.json();

        resultArea.innerText = data.result;

    } catch (error) {
        console.log(error);
        resultArea.innerText = "線路繁忙，請稍後重試。"
    }
}

evalBtn.addEventListener('click', debounce(evalCode,200));