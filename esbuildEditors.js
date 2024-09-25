/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

// 原始基礎由微軟 Monaco Editor Opensource 提供
// 另基於本專案需求進行微幅更動


const esbuild = require('esbuild');
const path = require('path');


const workerEntryPoints = [
	'vs/language/typescript/ts.worker.js',
	'vs/editor/editor.worker.js'
];

build({
	entryPoints: workerEntryPoints.map((entry) => `./node_modules/monaco-editor/esm/${entry}`),
	bundle: true,
	format: 'iife',
	outbase: './node_modules/monaco-editor/esm/',
	outdir: path.join(__dirname, 'static/editors')
});

build({
	entryPoints: ['./src/scripts/editors/collab.js'],
	bundle: true,
	format: 'iife',
	outdir: path.join(__dirname, 'static/editors'),
	loader: {
		'.ttf': 'file'
	}
});

build({
	entryPoints: ['./src/scripts/editors/individual.js'],
	bundle: true,
	format: 'iife',
	outdir: path.join(__dirname, 'static/editors'),
	loader: {
		'.ttf': 'file'
	}
});

/**
 * @param {import ('esbuild').BuildOptions} opts
 */
function build(opts) {
	esbuild.build(opts).then((result) => {
		if (result.errors.length > 0) {
			console.error(result.errors);
		}
		if (result.warnings.length > 0) {
			console.error(result.warnings);
		}
	});
}