// Скрипт для сворачивания/разворачивания блоков профиля в мобильной версии

document.addEventListener('DOMContentLoaded', function () {
    // Храним состояние вручную для каждого блока
    var state = {
        personal: null,
        contact: null,
        family: null
    };

    // 1. Блок с именем, фамилией, отчеством и кнопкой
    var personalInfo = document.querySelector('.personal-info');
    if (personalInfo) {
        var nameToggleBtn = document.createElement('button');
        nameToggleBtn.className = 'name-toggle-btn';
        nameToggleBtn.setAttribute('aria-label', 'Показать/скрыть имя и фамилию');
        nameToggleBtn.innerHTML = '<span class="arrow"></span>';
        personalInfo.parentNode.insertBefore(nameToggleBtn, personalInfo);

        function isMobile() { return window.innerWidth <= 600; }
        function setNameCollapsed(collapsed, manual) {
            if (collapsed) {
                personalInfo.style.display = 'none';
                nameToggleBtn.classList.add('collapsed');
            } else {
                personalInfo.style.display = '';
                nameToggleBtn.classList.remove('collapsed');
            }
            if (manual) state.personal = collapsed;
        }
        setNameCollapsed(isMobile(), false);
        nameToggleBtn.addEventListener('click', function () {
            var isCollapsed = personalInfo.style.display === 'none';
            setNameCollapsed(!isCollapsed, true);
        });
    }

    // 2. Блок с контактной информацией и кнопкой
    var contactInfo = document.querySelector('.contact-info');
    if (contactInfo) {
        var contactToggleBtn = document.createElement('button');
        contactToggleBtn.className = 'contact-toggle-btn';
        contactToggleBtn.setAttribute('aria-label', 'Показать/скрыть контакты');
        contactToggleBtn.innerHTML = '<span class="arrow"></span>';
        contactInfo.parentNode.insertBefore(contactToggleBtn, contactInfo);

        function isMobile2() { return window.innerWidth <= 600; }
        function setContactCollapsed(collapsed, manual) {
            if (collapsed) {
                contactInfo.style.display = 'none';
                contactToggleBtn.classList.add('collapsed');
            } else {
                contactInfo.style.display = '';
                contactToggleBtn.classList.remove('collapsed');
            }
            if (manual) state.contact = collapsed;
        }
        setContactCollapsed(isMobile2(), false);
        contactToggleBtn.addEventListener('click', function () {
            var isCollapsed = contactInfo.style.display === 'none';
            setContactCollapsed(!isCollapsed, true);
        });
    }

    // 3. Блок с семьей (сворачивать только до блока с паролем, но не hr.section-line)
    var familySection = document.querySelector('.family-section');
    var passwordInfo = document.querySelector('.password-info');
    if (familySection && passwordInfo) {
        var familyToggleBtn = document.createElement('button');
        familyToggleBtn.className = 'family-toggle-btn';
        familyToggleBtn.setAttribute('aria-label', 'Показать/скрыть семью');
        familyToggleBtn.innerHTML = '<span class="arrow"></span>';
        familySection.parentNode.insertBefore(familyToggleBtn, familySection);

        // Собираем все элементы в familySection до passwordInfo, кроме hr.section-line
        var toToggle = [];
        for (var i = 0; i < familySection.children.length; i++) {
            var el = familySection.children[i];
            if (el === passwordInfo) break;
            if (!(el.tagName === 'HR' && el.classList.contains('section-line'))) {
                toToggle.push(el);
            }
        }

        function isMobile3() { return window.innerWidth <= 600; }
        function setFamilyCollapsed(collapsed, manual) {
            toToggle.forEach(function(el) {
                el.style.display = collapsed ? 'none' : '';
            });
            if (collapsed) {
                familyToggleBtn.classList.add('collapsed');
            } else {
                familyToggleBtn.classList.remove('collapsed');
            }
            if (manual) state.family = collapsed;
        }
        setFamilyCollapsed(isMobile3(), false);
        familyToggleBtn.addEventListener('click', function () {
            var isCollapsed = toToggle[0].style.display === 'none';
            setFamilyCollapsed(!isCollapsed, true);
        });
    }

    // Глобальный обработчик для сброса скрытия на десктопе
    window.addEventListener('resize', function () {
        if (window.innerWidth > 600) {
            // Всегда раскрываем все секции и сбрасываем состояние
            if (personalInfo) {
                personalInfo.style.display = '';
                if (nameToggleBtn) nameToggleBtn.classList.remove('collapsed');
                state.personal = null;
            }
            if (contactInfo) {
                contactInfo.style.display = '';
                if (contactToggleBtn) contactToggleBtn.classList.remove('collapsed');
                state.contact = null;
            }
            if (familySection && toToggle && toToggle.length) {
                toToggle.forEach(function(el) { el.style.display = ''; });
                if (familyToggleBtn) familyToggleBtn.classList.remove('collapsed');
                state.family = null;
            }
        }
    });
});
