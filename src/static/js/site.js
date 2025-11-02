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
 * 注意：语言切换现在完全由模板处理，不需要JavaScript干预
 * 模板中的表单会直接提交到正确的URL，包括URL_PREFIX
 */

/**
 * 初始化语言切换器
 * 移除JavaScript处理，让表单自然提交
 */
function initLanguageSwitcher() {
    // 语言切换现在完全由模板中的表单处理
    // 不需要JavaScript干预，确保URL_PREFIX正确处理
}

// 初始化语言切换器
initLanguageSwitcher();