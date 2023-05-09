window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        codeStyle: function () {
            let codeBlocks = document.querySelectorAll('pre code');
            for (let i = 0; i < codeBlocks.length; i++) {
                // hljs.highlightBlock(codeBlocks[i]);
                codeBlocks[i].classList.add('rounded-lg', 'my-4', 'bg-slate-700', 'relative');

                const copyButton = document.createElement('img');
                copyButton.className = 'h-6 absolute top-0 right-0 m-2 text-slate-300 text-sm hover:text-slate-100 bg-slate-600 hover:bg-slate-500 rounded-md cursor-pointer p-1';
                // copyButton.textContent = 'Copy';
                copyButton.src = 'assets/copy_icon.png';

                console.log('copyButton')
                console.log(copyButton)

                copyButton.addEventListener('click', function() {
                    const codeContent = codeBlocks[i].textContent;
                    navigator.clipboard.writeText(codeContent).then(function() {
                        // alert('Code copied to clipboard!');
                    });
                });

                codeBlocks[i].appendChild(copyButton);
                // codeBlocks[i].insertBefore(copyButton, codeBlocks[i]);
                console.log('this is codeBlocks[i]')
                console.log(codeBlocks[i]);

            }

            let inlineCodeBlocks = document.querySelectorAll('code');
            for (let i = 0; i < inlineCodeBlocks.length; i++) {
                inlineCodeBlocks[i].classList.add('font-bold');
            }

        }
    }
});
