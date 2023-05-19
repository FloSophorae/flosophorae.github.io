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
var preview = document.getElementById('preview')

// 实时更新浏览区域
function updatePreview() {
    markdownText = preview.dataset.body;
    var htmlText = marked.parse(markdownText);
    preview.innerHTML = htmlText;
}
updatePreview();

// 安全删除文章:layui提示框
function confirm_safe_delete() {
    layer.open({
        title: "Ensure Delete",
        content: "Are your sure to delete this article?",
        yes: function (index, layero) {
            $('form#safe_delete button').click();
            layero.close(index);
        }
    })
}

var links = document.querySelectorAll("#preview a"); // 获取页面中所有的链接

for (var i = 0; i < links.length; i++) {
  links[i].setAttribute("target", "_blank"); // 为每个链接设置 target="_blank"
}
