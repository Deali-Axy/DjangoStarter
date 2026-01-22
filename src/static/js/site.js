// 初始化主题
function initTheme() {
    // 1. 获取当前主题 (优先从 localStorage 获取，否则跟随系统偏好)
    const theme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'business' : 'corporate');
    
    // 2. 应用主题
    applyTheme(theme);
    
    // 3. 同步 UI 状态 (选中对应的单选按钮)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => syncThemeUI(theme));
    } else {
        syncThemeUI(theme);
    }
}

// 应用主题并持久化
function applyTheme(theme) {
    // 设置 data-theme 属性 (DaisyUI 核心)
    document.documentElement.setAttribute('data-theme', theme);
    
    // 保存到 localStorage
    localStorage.setItem('theme', theme);
    
    // 处理 Tailwind 的 dark 类 (用于兼容部分依赖 dark 类的工具类)
    const darkThemes = [
        'business', 'dark', 'synthwave', 'halloween', 'forest', 'aqua', 
        'black', 'luxury', 'dracula', 'night', 'coffee', 'dim', 'sunset'
    ];
    
    if (darkThemes.includes(theme)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
}

// 同步 UI 选中状态
function syncThemeUI(theme) {
    const themeRadios = document.querySelectorAll('.theme-controller');
    themeRadios.forEach(radio => {
        if (radio.value === theme) {
            radio.checked = true;
        }
    });
}

// 初始化
initTheme();

// 监听主题切换事件
// DaisyUI 的 theme-controller 会自动更新 DOM，但我们需要拦截事件以进行持久化
document.addEventListener('change', (e) => {
    if (e.target.classList.contains('theme-controller')) {
        const newTheme = e.target.value;
        applyTheme(newTheme);
    }
});

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
