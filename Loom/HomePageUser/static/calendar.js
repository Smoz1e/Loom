function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            document.body.classList.toggle('sidebar-active');
            sidebar.classList.toggle('active');
        }

        // Обработчики событий
        document.getElementById('sidebarToggle').addEventListener('click', toggleSidebar);
        document.getElementById('sidebarClose').addEventListener('click', toggleSidebar);

        // Закрытие при клике вне панели
        document.addEventListener('click', (e) => {
            const sidebar = document.getElementById('sidebar');
            if (sidebar.classList.contains('active') && 
                !e.target.closest('#sidebar') && 
                !e.target.closest('#sidebarToggle')) {
                toggleSidebar();
            }
        });

        // Открытие/закрытие модального окна добавления задачи
        const addTaskBtn = document.getElementById('addTaskButton');
        const modalOverlay = document.getElementById('modalOverlay');
        const closeBtn = document.getElementById('closeModalBtn');
        const cancelBtn = document.getElementById('cancelBtn');

        // Получаем выбранную дату из Django (selected_date)
        const selectedDate = "{{ selected_date|date:'Y-m-d' }}";

        function setModalDateToSelected() {
          const dateInput = document.getElementById('dateInput');
          if (dateInput) {
            dateInput.value = selectedDate;
          }
        }

        addTaskBtn.onclick = function() {
          showModal();
          setModalDateToSelected();
        };

        function showModal() {
          modalOverlay.style.display = 'block';
          setTimeout(() => modalOverlay.classList.add('active'), 10);
          resetFormStyles && resetFormStyles();
        }
        function closeModal() {
          modalOverlay.classList.remove('active');
          setTimeout(() => modalOverlay.style.display = 'none', 200);
        }
        closeBtn.onclick = closeModal;
        cancelBtn.onclick = closeModal;
        window.onclick = (e) => {
          if (e.target === modalOverlay) {
            closeModal();
          }
        };

        // --- CATEGORY DROPDOWN LOGIC ---
        const categoryList = document.getElementById('categoryList');
        const categoryLabel = document.getElementById('categoryLabel');
        const selectedCategoryDot = document.getElementById('selectedCategoryDot');
        const categoryToggle = document.getElementById('categoryToggle');
        const categoryArrow = document.getElementById('categoryArrow');

        function toggleCategoryList() {
          const isOpen = categoryList.style.display === 'block';
          categoryList.style.display = isOpen ? 'none' : 'block';
          categoryArrow.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
          categoryArrow.style.transition = 'transform 0.2s ease';
        }

        categoryToggle.addEventListener('click', function(e) {
          if (e.target === categoryArrow || e.target.classList.contains('category-arrow')) {
            toggleCategoryList();
            e.stopPropagation();
          } else if (!e.target.closest('.category-item')) {
            toggleCategoryList();
          }
        });

        categoryList.addEventListener('click', function(e) {
          const item = e.target.closest('.category-item');
          if (item) {
            document.querySelectorAll('.category-item').forEach(el => el.classList.remove('selected'));
            item.classList.add('selected');
            const categoryName = item.getAttribute('data-value');
            const dot = item.querySelector('.category-dot');
            let dotColor = '';
            if (dot) {
              dotColor = Array.from(dot.classList).find(cls => cls !== 'category-dot');
            }
            categoryLabel.textContent = categoryName;
            categoryToggle.classList.add('has-selection');
            selectedCategoryDot.className = 'selected-category-dot ' + (dotColor || '');
            selectedCategoryDot.style.display = 'inline-block';
            categoryList.style.display = 'none';
            categoryArrow.style.transform = 'rotate(0deg)';
          }
        });

        document.addEventListener('click', function(e) {
          if (!categoryToggle.contains(e.target) && !e.target.closest('.category-list')) {
            categoryList.style.display = 'none';
            categoryArrow.style.transform = 'rotate(0deg)';
          }
        });

        // --- AJAX сохранение задачи из модального окна ---
        document.querySelector('.modal-btn.save').onclick = async function(e) {
          e.preventDefault();
          const modal = document.querySelector('.modal');
          const title = modal.querySelector('.event-title').value.trim();
          const description = '';
          const date = modal.querySelector('#dateInput').value.trim();
          const start_time = modal.querySelector('#startTime').value.trim();
          const end_time = modal.querySelector('#endTime').value.trim();
          const category = document.getElementById('categoryLabel').textContent.trim() === 'Выбрать тему' ? '' : document.getElementById('categoryLabel').textContent.trim();
          const timezone = document.getElementById('timezoneSelected').textContent.trim() === 'Часовой пояс' ? '' : document.getElementById('timezoneSelected').textContent.trim();
          const is_private = document.getElementById('privateCheckbox').classList.contains('checked');
          let repeat_type = '';
          let repeat_days = '';
          const selectedRepeat = document.querySelector('.repeat-option.selected');
          if (selectedRepeat) repeat_type = selectedRepeat.textContent.trim();
          const selectedDays = Array.from(document.querySelectorAll('.repeat-day.selected')).map(d => d.textContent.trim());
          if (selectedDays.length) repeat_days = selectedDays.join(',');
          let participants = '';
          const partList = document.querySelectorAll('.participants-list .participant-chip');
          if (partList.length) participants = Array.from(partList).map(p => p.textContent.trim()).join(',');
          const priority = modal.querySelector('input[name="priority"]:checked')?.value || 'normal';

          const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || (document.cookie.match(/csrftoken=([^;]+)/)||[])[1];
          const formData = new FormData();
          formData.append('title', title);
          formData.append('description', description);
          formData.append('date', date);
          formData.append('start_time', start_time);
          formData.append('end_time', end_time);
          formData.append('category', category);
          formData.append('timezone', timezone);
          formData.append('is_private', is_private);
          formData.append('repeat_type', repeat_type);
          formData.append('repeat_days', repeat_days);
          formData.append('participants', participants);
          formData.append('priority', priority);

          const response = await fetch(window.location.href, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken, 'X-Requested-With': 'XMLHttpRequest' },
            body: formData
          });
          const data = await response.json();
          if (data.success) {
            closeModal();
            window.location.reload();
          } else if (data.errors) {
            alert(data.errors.join('\n'));
          }
        }

        // Удаление задачи через AJAX
        document.querySelectorAll('.delete-task-btn').forEach(btn => {
            btn.addEventListener('click', async function(e) {
                e.stopPropagation();
                const taskId = this.getAttribute('data-task-id');
                if (!confirm('Удалить задачу?')) return;
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || (document.cookie.match(/csrftoken=([^;]+)/)||[])[1];
                const response = await fetch('/api/delete_personal_task/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: taskId })
                });
                const data = await response.json();
                if (data.success) {
                    // Удаляем задачу из sidebar
                    this.closest('.task-item').remove();
                    // Удаляем задачу из основной сетки календаря
                    document.querySelectorAll('.task-container-cases[data-task-id="' + taskId + '"]').forEach(el => el.remove());
                } else {
                    alert(data.error || 'Ошибка удаления');
                }
            });
        });

        // Отметка задачи как выполненной/невыполненной
        document.querySelectorAll('.complete-task-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', async function() {
                const taskId = this.getAttribute('data-task-id');
                const isChecked = this.checked;
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || (document.cookie.match(/csrftoken=([^;]+)/)||[])[1];
                await fetch('/api/toggle_task_completion/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: taskId, is_completed: isChecked })
                });
                // Обновляем интерфейс: добавляем/убираем класс completed у всех элементов с этим task-id
                document.querySelectorAll('[data-task-id="' + taskId + '"]').forEach(el => {
                    if (isChecked) {
                        el.classList.add('completed');
                    } else {
                        el.classList.remove('completed');
                    }
                });
            });
        });

        // --- Открытие/закрытие модального окна чата с ИИ ---
    const aiChatOpenBtn = document.getElementById('aiChatOpenBtn');
    const modalAiChat = document.getElementById('modalAiChat');
    const aiChatCloseBtn = document.getElementById('aiChatCloseBtn');
    aiChatOpenBtn.onclick = () => {
      modalAiChat.classList.add('active');
      setTimeout(()=>{
        document.getElementById('aiChatInput').focus();
      }, 100);
    };
    aiChatCloseBtn.onclick = () => { modalAiChat.classList.remove('active'); };
    window.addEventListener('keydown', e => {
      if (e.key === 'Escape' && modalAiChat.classList.contains('active')) modalAiChat.classList.remove('active');
    });
    modalAiChat.addEventListener('click', e => {
      if (e.target === modalAiChat) modalAiChat.classList.remove('active');
    });

    // --- Логика чата с ИИ (frontend, без реального ИИ) ---
    const aiChatForm = document.getElementById('aiChatForm');
    const aiChatInput = document.getElementById('aiChatInput');
    const aiChatSendBtn = document.getElementById('aiChatSendBtn');
    const aiChatMessages = document.getElementById('aiChatMessages');
    aiChatInput.addEventListener('input', () => {
      aiChatSendBtn.disabled = aiChatInput.value.trim().length === 0;
    });
    aiChatForm.onsubmit = async function(e) {
      e.preventDefault();
      const text = aiChatInput.value.trim();
      if (!text) return;
      addAiMessage(text, 'user');
      aiChatInput.value = '';
      aiChatSendBtn.disabled = true;
      aiChatMessages.scrollTop = aiChatMessages.scrollHeight;
      // Имитация ответа ИИ
      setTimeout(() => {
        addAiMessage('Это пример ответа ИИ. (Интеграция с реальным ИИ на сервере)', 'bot');
        aiChatMessages.scrollTop = aiChatMessages.scrollHeight;
      }, 900);
    };
    function addAiMessage(text, who) {
      const msg = document.createElement('div');
      msg.className = 'ai-message ' + who;
      msg.textContent = text;
      aiChatMessages.appendChild(msg);
    }