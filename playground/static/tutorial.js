/**
 * 段言 (Duan) 交互式教程系统 v4.1
 */

const TUTORIAL_STORAGE_KEY = 'duan_tutorial_progress';

// 教程数据
const TUTORIAL_LESSONS = [
    // ============================
    // 第一章：入门基础
    // ============================
    {
        id: 'ch1_hello',
        chapter: '第一章：入门基础',
        title: '1.1 你好，段言！',
        description: '用「打印」语句输出你的第一行段言代码。',
        task: '请在编辑器中输入代码，打印 "你好，段言！"。',
        template: '打印 "你好，段言！"。\n',
        expected: '你好，段言！',
        hint: '使用「打印」关键字，后面跟上要输出的内容，以句号结束。',
        keywords: ['打印'],
        level: 'beginner'
    },
    {
        id: 'ch1_variable',
        chapter: '第一章：入门基础',
        title: '1.2 变量定义',
        description: '学习用「设」关键字定义变量。',
        task: '定义一个变量「姓名」为 "小明"，然后打印它。',
        template: '设 姓名 为 "小明"。\n打印 姓名。\n',
        expected: '小明',
        hint: '「设 变量名 为 值。」是段言定义变量的标准语法。',
        keywords: ['设', '为'],
        level: 'beginner'
    },
    {
        id: 'ch1_calc',
        chapter: '第一章：入门基础',
        title: '1.3 简单计算',
        description: '学习使用算术运算符进行基本计算。',
        task: '计算 10 + 20 * 3 的结果并打印。',
        template: '设 结果 为 10 + 20 * 3。\n打印 结果。\n',
        expected: '70',
        hint: '算术运算符包括 +（加）、-（减）、*（乘）、/（除），运算优先级与数学一致。',
        keywords: ['设', '为', '打印'],
        level: 'beginner'
    },
    {
        id: 'ch1_string',
        chapter: '第一章：入门基础',
        title: '1.4 字符串操作',
        description: '学习字符串的基本操作，包括拼接。',
        task: '将 "段" 和 "言" 拼接起来，然后打印。',
        template: '设 姓 为 "段"。\n设 名 为 "言"。\n设 全名 为 姓 + 名。\n打印 全名。\n',
        expected: '段言',
        hint: '用 + 号可以拼接两个字符串。',
        keywords: ['设', '打印'],
        level: 'beginner'
    },

    // ============================
    // 第二章：L0 核心关键字
    // ============================
    {
        id: 'ch2_ruo',
        chapter: '第二章：L0 核心关键字',
        title: '2.1 条件语句「若」',
        description: '学习 L0 单字关键字「若」进行条件判断。',
        task: '判断 10 是否大于 5，如果是则打印 "成立"。',
        template: '设 甲 为 10。\n若 甲 > 5 则：\n  打印 "成立"。\n结束。\n',
        expected: '成立',
        hint: '「若 条件 则：」是 L0 的条件语句，用「结束」收尾。',
        keywords: ['若', '则', '结束'],
        level: 'intermediate'
    },
    {
        id: 'ch2_bian',
        chapter: '第二章：L0 核心关键字',
        title: '2.2 遍历循环「遍」',
        description: '学习 L0 关键字「遍」进行列表遍历。',
        task: '用「遍」遍历列表 [1, 2, 3]，打印每个元素。',
        template: '设 数据 为 [1, 2, 3]。\n遍 元素 之 数据：\n  打印 元素。\n结束。\n',
        expected: '1\n2\n3',
        hint: '「遍 变量 之 列表：」是 L0 的遍历语法。',
        keywords: ['遍', '之', '结束'],
        level: 'intermediate'
    },
    {
        id: 'ch2_duan',
        chapter: '第二章：L0 核心关键字',
        title: '2.3 段落（函数）「段」',
        description: '学习 L0 关键字「段」定义函数。',
        task: '定义一个段「加倍」，接收一个参数，返回其两倍值。然后调用并打印。',
        template: '段 加倍(数)：\n  返回 数 * 2。\n结束。\n\n打印 加倍(21)。\n',
        expected: '42',
        hint: '「段 函数名(参数)：」定义函数，用「返回」返回值。',
        keywords: ['段', '返回', '结束'],
        level: 'intermediate'
    },
    {
        id: 'ch2_shi',
        chapter: '第二章：L0 核心关键字',
        title: '2.4 异常处理「试」',
        description: '学习 L0 关键字「试」进行异常捕获。',
        task: '尝试执行 1/0，捕获异常后打印 "除零错误"。',
        template: '试：\n  设 甲 为 1 / 0。\n捕：\n  打印 "除零错误"。\n结束。\n',
        expected: '除零错误',
        hint: '「试：...捕：...结束。」是 L0 的异常处理语法。',
        keywords: ['试', '捕', '结束'],
        level: 'intermediate'
    },

    // ============================
    // 第三章：L1/L2 文体风格
    // ============================
    {
        id: 'ch3_l1_intro',
        chapter: '第三章：L1/L2 文体风格',
        title: '3.1 L1 白话体入门',
        description: 'L1（白话体）使用双字关键字和中文标点，适合教学和初学者。',
        task: '用 L1 风格写一段代码：定义变量，判断条件，打印结果。',
        template: '如果 甲 > 5 那么：\n  打印 "大于5"。\n否则：\n  打印 "不大于5"。\n结束。\n',
        expected: '大于5',
        hint: 'L1 使用双字关键字「如果」「那么」「否则」「打印」等，标点使用中文句号。',
        keywords: ['如果', '那么', '否则', '打印', '结束'],
        level: 'beginner'
    },
    {
        id: 'ch3_l2_intro',
        chapter: '第三章：L1/L2 文体风格',
        title: '3.2 L2 文言体入门',
        description: 'L2（文言体）使用 L0 单字关键字和英文标点，适合商业项目和熟练开发者。',
        task: '用 L2 风格写同样的条件判断，使用 L0 单字关键字。',
        template: '设 甲 为 10。\n若 甲 > 5 则：\n  打印 "大于5"。\n否：\n  打印 "不大于5"。\n结束。\n',
        expected: '大于5',
        hint: 'L2 使用 L0 单字关键字「若」「否」等，表达式更简洁。',
        keywords: ['若', '则', '否', '结束'],
        level: 'intermediate'
    },
    {
        id: 'ch3_l1_l2_mix',
        chapter: '第三章：L1/L2 文体风格',
        title: '3.3 风格混用与兼容',
        description: '段言支持 L1 和 L2 风格混用，新旧关键字可以共存。',
        task: '混用 L1 和 L2 关键字：用「设」定义变量，用「如果」判断，用「打印」输出。',
        template: '设 分数 为 85。\n如果 分数 >= 60 那么：\n  打印 "及格"。\n否则：\n  打印 "不及格"。\n结束。\n',
        expected: '及格',
        hint: '段言 v4.0 同时支持 L0 单字和 L1 双字关键字，可以自由混用。',
        keywords: ['设', '如果', '那么', '否则', '打印', '结束'],
        level: 'intermediate'
    },

    // ============================
    // 第四章：L3 领域嵌入
    // ============================
    {
        id: 'ch4_math',
        chapter: '第四章：L3 领域嵌入',
        title: '4.1 数学表达式',
        description: 'L3 数学领域：直接使用数学表达式进行计算。',
        task: '计算 2 的 10 次方，然后打印结果。',
        template: '设 甲 为 2 ** 10。\n打印 甲。\n',
        expected: '1024',
        hint: '段言支持 ** 幂运算，以及所有标准数学运算符。',
        keywords: ['设', '打印'],
        level: 'advanced'
    },
    {
        id: 'ch4_regex',
        chapter: '第四章：L3 领域嵌入',
        title: '4.2 正则表达式',
        description: 'L3 正则领域：使用正则表达式匹配文本。',
        task: '用正则判断字符串 "abc123" 是否包含数字。',
        template: '引 Python:\nimport re\nresult = "yes" if re.search(r"\\d+", "abc123") else "no"\n出 result\n\n打印 result。\n',
        expected: 'yes',
        hint: '用「引 Python:」块嵌入 Python 正则代码，用「出」导出变量。',
        keywords: ['引', '出', '打印'],
        level: 'advanced'
    },

    // ============================
    // 第五章：L4 外部语言引用
    // ============================
    {
        id: 'ch5_python',
        chapter: '第五章：L4 外部语言引用',
        title: '5.1 Python 代码嵌入',
        description: 'L4 层：使用「引 Python:」块嵌入 Python 代码。',
        task: '在嵌入块中计算斐波那契数列第 10 项，并导出让段言打印。',
        template: '引 Python:\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n出 fib\n\n设 结果 为 fib(10)。\n打印 结果。\n',
        expected: '55',
        hint: '用「引 Python:」定义 Python 函数，用「出」导出，段言代码可直接调用。',
        keywords: ['引', '出', '设', '打印'],
        level: 'advanced'
    },
    {
        id: 'ch5_import',
        chapter: '第五章：L4 外部语言引用',
        title: '5.2 模块导入「导」',
        description: '学习使用「导」关键字导入模块和标准库。',
        task: '导入 Python 的 math 模块，计算 π 的值并打印。',
        template: '引 Python:\nimport math\n出 math\n\n设 圆周率 为 math.pi。\n打印 圆周率。\n',
        expected: '3.141592653589793',
        hint: '「导」可以导入段言模块，「引 Python:」可以导入 Python 标准库。',
        keywords: ['引', '出', '设', '打印'],
        level: 'advanced'
    },

    // ============================
    // 第六章：综合实战
    // ============================
    {
        id: 'ch6_sort',
        chapter: '第六章：综合实战',
        title: '6.1 冒泡排序',
        description: '综合运用所学知识，实现冒泡排序算法。',
        task: '用 L2 风格实现冒泡排序，对 [5, 2, 8, 1, 9] 排序并打印。',
        template: '段 冒泡排序(列表)：\n  设 长度 为 列表之长度。\n  遍 甲 之 范围(长度)：\n    遍 乙 之 范围(长度 - 甲 - 1)：\n      若 列表[乙] > 列表[乙 + 1] 则：\n        设 临时 为 列表[乙]。\n        列表[乙] 为 列表[乙 + 1]。\n        列表[乙 + 1] 为 临时。\n      结束。\n    结束。\n  结束。\n  返回 列表。\n结束。\n\n设 数据 为 [5, 2, 8, 1, 9]。\n打印 冒泡排序(数据)。\n',
        expected: '[1, 2, 5, 8, 9]',
        hint: '使用「遍」嵌套循环遍历，用「若」判断大小，用临时变量交换元素。',
        keywords: ['段', '遍', '若', '为', '返回', '结束'],
        level: 'advanced'
    },
    {
        id: 'ch6_class',
        chapter: '第六章：综合实战',
        title: '6.2 面向对象编程',
        description: '学习用「类」关键字定义类，实现面向对象编程。',
        task: '定义一个「计数器」类，有「计数」属性和「增加」方法，创建实例并测试。',
        template: '引 Python:\nclass Counter:\n    def __init__(self):\n        self.count = 0\n    def add(self, n=1):\n        self.count += n\n        return self.count\n出 Counter\n\n设 计数器 为 Counter()。\n打印 计数器之add(1)。\n打印 计数器之add(3)。\n打印 计数器之count。\n',
        expected: '1\n4\n4',
        hint: 'L4 嵌入 Python 类定义，用「出」导出类的构造函数，段言中可直接使用。',
        keywords: ['引', '出', '设', '打印'],
        level: 'advanced'
    },
    {
        id: 'ch6_list',
        chapter: '第六章：综合实战',
        title: '6.3 列表推导式',
        description: '学习使用列表推导式快速生成列表。',
        task: '用列表推导式生成 [1, 4, 9, 16, 25]（1到5的平方），并打印。',
        template: '引 Python:\nsquares = [x * x for x in range(1, 6)]\n出 squares\n\n打印 squares。\n',
        expected: '[1, 4, 9, 16, 25]',
        hint: '在「引 Python:」块中使用 Python 列表推导式，用「出」导出结果。',
        keywords: ['引', '出', '打印'],
        level: 'advanced'
    }
];

// 教程状态管理
const TutorialState = {
    lessons: TUTORIAL_LESSONS,
    currentIndex: 0,
    completed: {},

    init() {
        const saved = localStorage.getItem(TUTORIAL_STORAGE_KEY);
        if (saved) {
            try {
                const data = JSON.parse(saved);
                this.completed = data.completed || {};
                this.currentIndex = data.currentIndex || 0;
            } catch (e) {
                this.completed = {};
                this.currentIndex = 0;
            }
        }
    },

    save() {
        localStorage.setItem(TUTORIAL_STORAGE_KEY, JSON.stringify({
            completed: this.completed,
            currentIndex: this.currentIndex
        }));
    },

    markCompleted(lessonId) {
        this.completed[lessonId] = true;
        this.save();
    },

    isCompleted(lessonId) {
        return !!this.completed[lessonId];
    },

    getProgress() {
        const total = this.lessons.length;
        const done = Object.keys(this.completed).length;
        return { done, total, percent: Math.round((done / total) * 100) };
    },

    getCurrentLesson() {
        return this.lessons[this.currentIndex];
    },

    nextLesson() {
        if (this.currentIndex < this.lessons.length - 1) {
            this.currentIndex++;
            this.save();
            return this.getCurrentLesson();
        }
        return null;
    },

    prevLesson() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.save();
            return this.getCurrentLesson();
        }
        return null;
    },

    jumpTo(index) {
        if (index >= 0 && index < this.lessons.length) {
            this.currentIndex = index;
            this.save();
            return this.getCurrentLesson();
        }
        return null;
    },

    reset() {
        this.completed = {};
        this.currentIndex = 0;
        this.save();
    }
};

// 初始化
TutorialState.init();

// =============================================================================
// 教程 UI
// =============================================================================

let tutorialOverlay = null;
let tutorialModal = null;

function openTutorial() {
    if (!tutorialOverlay) {
        createTutorialUI();
    }
    tutorialOverlay.classList.remove('hidden');
    renderTutorialLesson();
    renderTutorialSidebar();
}

function closeTutorial() {
    if (tutorialOverlay) {
        tutorialOverlay.classList.add('hidden');
    }
}

function createTutorialUI() {
    // 遮罩层
    tutorialOverlay = document.createElement('div');
    tutorialOverlay.className = 'tutorial-overlay hidden';
    tutorialOverlay.addEventListener('click', function(e) {
        if (e.target === tutorialOverlay) {
            closeTutorial();
        }
    });

    tutorialModal = document.createElement('div');
    tutorialModal.className = 'tutorial-modal';
    tutorialModal.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    tutorialModal.innerHTML = `
        <div class="tutorial-header">
            <div class="tutorial-header-left">
                <svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zM6.5 4.5h3v1.5h-3v-1.5zm0 3h3v1.5h-3v-1.5zm0 3h2v1.5h-2v-1.5z"/></svg>
                <span class="tutorial-title">段言交互式教程</span>
                <span class="tutorial-progress" id="tutorialProgress">0/20</span>
            </div>
            <div class="tutorial-header-right">
                <button class="btn btn-icon" onclick="resetTutorial()" title="重置进度">↺</button>
                <button class="btn btn-close" onclick="closeTutorial()" title="关闭">✕</button>
            </div>
        </div>
        <div class="tutorial-body">
            <div class="tutorial-sidebar" id="tutorialSidebar">
                <div class="tutorial-chapters"></div>
            </div>
            <div class="tutorial-content" id="tutorialContent">
                <div class="tutorial-loading">📖 加载教程中...</div>
            </div>
        </div>
        <div class="tutorial-footer">
            <button class="btn btn-small" id="tutorialPrevBtn" onclick="tutorialPrev()">◀ 上一课</button>
            <span class="tutorial-lesson-indicator" id="tutorialLessonIndicator">1 / 20</span>
            <button class="btn btn-small" id="tutorialNextBtn" onclick="tutorialNext()">下一课 ▶</button>
        </div>
    `;

    tutorialOverlay.appendChild(tutorialModal);
    document.body.appendChild(tutorialOverlay);
}

function renderTutorialSidebar() {
    const sidebar = document.getElementById('tutorialSidebar');
    if (!sidebar) return;

    const chapters = {};
    TutorialState.lessons.forEach((lesson, idx) => {
        if (!chapters[lesson.chapter]) {
            chapters[lesson.chapter] = [];
        }
        chapters[lesson.chapter].push({ ...lesson, index: idx });
    });

    let html = '';
    for (const [chapter, lessons] of Object.entries(chapters)) {
        html += `<div class="tutorial-chapter">
            <div class="tutorial-chapter-title">${chapter}</div>`;
        lessons.forEach(lesson => {
            const isCurrent = lesson.index === TutorialState.currentIndex;
            const isDone = TutorialState.isCompleted(lesson.id);
            const cls = isCurrent ? 'tutorial-lesson-link current' : 'tutorial-lesson-link';
            html += `<div class="${cls}" onclick="jumpToLesson(${lesson.index})">
                <span class="tutorial-lesson-dot">${isDone ? '✓' : (isCurrent ? '●' : '○')}</span>
                <span class="tutorial-lesson-name">${lesson.title}</span>
            </div>`;
        });
        html += '</div>';
    }
    sidebar.querySelector('.tutorial-chapters').innerHTML = html;
}

function renderTutorialLesson() {
    const content = document.getElementById('tutorialContent');
    const lesson = TutorialState.getCurrentLesson();
    if (!lesson || !content) return;

    const isDone = TutorialState.isCompleted(lesson.id);
    const levelLabels = {
        'beginner': '入门',
        'intermediate': '进阶',
        'advanced': '高级'
    };
    const levelColors = {
        'beginner': 'var(--accent-green)',
        'intermediate': 'var(--accent-blue)',
        'advanced': 'var(--accent-purple)'
    };

    content.innerHTML = `
        <div class="tutorial-lesson">
            <div class="tutorial-lesson-header">
                <span class="tutorial-lesson-chapter">${lesson.chapter}</span>
                <span class="tutorial-lesson-level" style="color:${levelColors[lesson.level]};border-color:${levelColors[lesson.level]}">${levelLabels[lesson.level] || lesson.level}</span>
                ${isDone ? '<span class="tutorial-lesson-done">✓ 已完成</span>' : ''}
            </div>
            <h2 class="tutorial-lesson-title">${lesson.title}</h2>
            <p class="tutorial-lesson-desc">${lesson.description}</p>
            <div class="tutorial-lesson-task">
                <div class="tutorial-task-label">🎯 任务</div>
                <p>${lesson.task}</p>
            </div>
            ${lesson.keywords ? `
            <div class="tutorial-lesson-keywords">
                <div class="tutorial-keywords-label">📝 本课关键字</div>
                <div class="tutorial-keywords-list">
                    ${lesson.keywords.map(kw => `<span class="tutorial-keyword">${kw}</span>`).join('')}
                </div>
            </div>` : ''}
            <div class="tutorial-lesson-actions">
                <button class="btn btn-primary" onclick="loadTutorialTemplate()">📥 加载模板代码</button>
                <button class="btn btn-run" onclick="checkTutorialAnswer()">✅ 运行并验证</button>
            </div>
            <div class="tutorial-lesson-hint" id="tutorialHint" style="display:none">
                <div class="tutorial-hint-label">💡 提示</div>
                <p>${lesson.hint || ''}</p>
            </div>
            <div class="tutorial-lesson-result" id="tutorialResult" style="display:none"></div>
        </div>
    `;

    // 更新底部导航
    const indicator = document.getElementById('tutorialLessonIndicator');
    const prevBtn = document.getElementById('tutorialPrevBtn');
    const nextBtn = document.getElementById('tutorialNextBtn');
    if (indicator) {
        indicator.textContent = `${TutorialState.currentIndex + 1} / ${TutorialState.lessons.length}`;
    }
    if (prevBtn) {
        prevBtn.disabled = TutorialState.currentIndex === 0;
    }
    if (nextBtn) {
        nextBtn.disabled = TutorialState.currentIndex >= TutorialState.lessons.length - 1;
    }

    // 更新进度
    const progress = document.getElementById('tutorialProgress');
    if (progress) {
        const p = TutorialState.getProgress();
        progress.textContent = `${p.done}/${p.total}`;
    }
}

function loadTutorialTemplate() {
    const lesson = TutorialState.getCurrentLesson();
    if (!lesson || !lesson.template) return;
    if (editor) {
        editor.setValue(lesson.template);
        showToast('模板代码已加载到编辑器', 'info');
    }
}

async function checkTutorialAnswer() {
    const lesson = TutorialState.getCurrentLesson();
    if (!lesson || !editor) return;

    const code = editor.getValue();
    if (!code.trim()) {
        showToast('请先在编辑器中输入代码', 'warning');
        return;
    }

    const resultDiv = document.getElementById('tutorialResult');
    const hintDiv = document.getElementById('tutorialHint');

    if (resultDiv) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '<div class="tutorial-checking">⏳ 正在运行代码...</div>';
    }

    try {
        const resp = await fetch(API_BASE + '/api/demos/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source: code })
        });
        const data = await resp.json();

        if (data.error) {
            if (resultDiv) {
                resultDiv.innerHTML = `<div class="tutorial-fail">
                    <div class="tutorial-fail-title">❌ 代码有错误</div>
                    <pre class="tutorial-error-output">${escapeHtml(data.error)}</pre>
                </div>`;
            }
            if (hintDiv) hintDiv.style.display = 'block';
            return;
        }

        const output = (data.output || '').trim();
        const expected = (lesson.expected || '').trim();

        if (output === expected) {
            if (resultDiv) {
                resultDiv.innerHTML = `<div class="tutorial-success">
                    <div class="tutorial-success-title">🎉 恭喜！答案正确！</div>
                    <pre class="tutorial-success-output">${escapeHtml(output)}</pre>
                </div>`;
            }
            TutorialState.markCompleted(lesson.id);
            renderTutorialSidebar();
            renderTutorialLesson();
            showToast('答案正确！课程已完成', 'success');
        } else {
            if (resultDiv) {
                resultDiv.innerHTML = `<div class="tutorial-fail">
                    <div class="tutorial-fail-title">🤔 输出不匹配</div>
                    <div class="tutorial-compare">
                        <div class="tutorial-compare-item">
                            <span class="tutorial-compare-label">期望输出：</span>
                            <pre>${escapeHtml(expected)}</pre>
                        </div>
                        <div class="tutorial-compare-item">
                            <span class="tutorial-compare-label">实际输出：</span>
                            <pre>${escapeHtml(output)}</pre>
                        </div>
                    </div>
                </div>`;
            }
            if (hintDiv) hintDiv.style.display = 'block';
        }
    } catch (e) {
        if (resultDiv) {
            resultDiv.innerHTML = `<div class="tutorial-fail">
                <div class="tutorial-fail-title">❌ 运行失败</div>
                <pre class="tutorial-error-output">${escapeHtml(e.message)}</pre>
            </div>`;
        }
    }
}

function tutorialNext() {
    const lesson = TutorialState.nextLesson();
    if (lesson) {
        renderTutorialLesson();
        renderTutorialSidebar();
        loadTutorialTemplate();
    }
}

function tutorialPrev() {
    const lesson = TutorialState.prevLesson();
    if (lesson) {
        renderTutorialLesson();
        renderTutorialSidebar();
        loadTutorialTemplate();
    }
}

function jumpToLesson(index) {
    const lesson = TutorialState.jumpTo(index);
    if (lesson) {
        renderTutorialLesson();
        renderTutorialSidebar();
        loadTutorialTemplate();
    }
}

function resetTutorial() {
    if (confirm('确定要重置所有教程进度吗？此操作不可撤销。')) {
        TutorialState.reset();
        renderTutorialLesson();
        renderTutorialSidebar();
        showToast('教程进度已重置', 'info');
    }
}

// 键盘快捷键
document.addEventListener('keydown', function(e) {
    // 检查教程是否打开
    if (tutorialOverlay && !tutorialOverlay.classList.contains('hidden')) {
        if (e.key === 'Escape') {
            closeTutorial();
        } else if (e.key === 'ArrowRight' && !e.ctrlKey && !e.metaKey) {
            e.preventDefault();
            tutorialNext();
        } else if (e.key === 'ArrowLeft' && !e.ctrlKey && !e.metaKey) {
            e.preventDefault();
            tutorialPrev();
        }
    }
});