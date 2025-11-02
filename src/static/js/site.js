// 检查用户偏好的主题并应用
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}

// 主题切换函数
function toggleDarkMode() {
    if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
        localStorage.theme = 'light';
    } else {
        document.documentElement.classList.add('dark');
        localStorage.theme = 'dark';
    }
}

/**
 * 语言切换功能
 * 处理语言切换表单的提交
 */
function switchLanguage(languageCode) {
    // 创建隐藏表单来提交语言切换请求
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/i18n/setlang/';
    
    // 添加CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken.value;
        form.appendChild(csrfInput);
    }
    
    // 添加语言代码
    const languageInput = document.createElement('input');
    languageInput.type = 'hidden';
    languageInput.name = 'language';
    languageInput.value = languageCode;
    form.appendChild(languageInput);
    
    // 添加next参数，保持在当前页面
    const nextInput = document.createElement('input');
    nextInput.type = 'hidden';
    nextInput.name = 'next';
    nextInput.value = window.location.pathname + window.location.search;
    form.appendChild(nextInput);
    
    // 提交表单
    document.body.appendChild(form);
    form.submit();
}

/**
 * 初始化语言切换器
 * 为语言切换链接添加点击事件处理器
 */
function initLanguageSwitcher() {
    document.addEventListener('DOMContentLoaded', function() {
        const languageLinks = document.querySelectorAll('[data-language-code]');
        
        languageLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const languageCode = this.getAttribute('data-language-code');
                switchLanguage(languageCode);
            });
        });
    });
}

// 初始化语言切换器
initLanguageSwitcher();