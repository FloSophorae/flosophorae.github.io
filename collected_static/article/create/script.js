/**
 * Marked.js：实时Markdown→HTML渲染
*/

hljs.highlightAll();
// 设置marked参数
marked.setOptions({
    renderer: new marked.Renderer(),
    gfm: true,
    tables: true,
    breaks: true,
    pedantic: false,
    sanitize: false,
    smartLists: true,
    smartypants: false,
    highlight(code) {
        return hljs.highlightAuto(code).value
    }
})
// 获取DOM元素
var editor = document.getElementById('editor')
var preview = document.getElementById('preview')

// 实时更新浏览区域
function updatePreview() {
    var markdownText = editor.value;
    var htmlText = marked.parse(markdownText);
    preview.innerHTML = htmlText;
}

// 注册输入事件监听器
editor.addEventListener('input', function () {
    updatePreview(); // 调用更新函数
})

/**
 * 可拖拽分隔栏
 */
edit_container = document.getElementById("editor")
const dragBar = document.querySelector('.drag-bar');
let isDragging = false;

dragBar.addEventListener('mousedown', function (e) {
    isDragging = true;
});

document.addEventListener('mousemove', function (e) {
    if (isDragging) {
        const x = e.pageX;
        const containerRect = document.querySelector('#create-form').getBoundingClientRect();
        const containerX = containerRect.x;
        const containerWidth = containerRect.width;
        const dragBarWidth = dragBar.getBoundingClientRect().width;
        const editorWidth = Math.min(Math.max(0, x - containerX - dragBarWidth / 2), containerWidth - dragBarWidth);
        edit_container.style.width = `${editorWidth}px`;
        preview.style.width = `${containerWidth - dragBarWidth - editorWidth}px`;
    }
});

document.addEventListener('mouseup', function (e) {
    isDragging = false;
});

/**
 * 提供Tab支持
 */

// 捕获Tab键
// 支持Tab缩进
editor.addEventListener('keydown', function (e) {
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        const value = this.value;

        // 在光标所在位置插入Tab符号
        this.value = value.substring(0, start) + '    ' + value.substring(end);
        // 将光标移动到插入后的位置
        this.selectionStart = this.selectionEnd = start + 4;
        // 利用js模拟用户输入
        const inputEvent = new Event('input', { bubbles: true });
        this.dispatchEvent(inputEvent);
    }
});


