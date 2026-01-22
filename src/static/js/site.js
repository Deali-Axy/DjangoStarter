// 检查用户偏好的主题并应用
function initTheme() {
    const theme = localStorage.theme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'business' : 'corporate');
    document.documentElement.setAttribute('data-theme', theme);
    if (theme === 'business') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
}
initTheme();

// 主题切换函数
function toggleDarkMode() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'business' ? 'corporate' : 'business';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.theme = newTheme;
    
    if (newTheme === 'business') {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
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
