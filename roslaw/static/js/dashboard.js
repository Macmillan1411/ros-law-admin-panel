$(document).ready(function() {
    // Get URL parameters from the data attributes we'll set in the HTML
    const activeChapter = $('#content-data').data('active-chapter');
    const activeSection = $('#content-data').data('active-section');
    const activeSubsection = $('#content-data').data('active-subsection');
    const dashboardUrl = $('#content-data').data('dashboard-url');

    // Initially hide all dropdown content
    $('.sections-container').hide();
    $('.subsections-container').hide();
    $('.qa-container').hide();

    $('.chapter-header').click(function(e) {
        e.preventDefault();
        const chapterId = $(this).data('id');

        if (chapterId == activeChapter) {

            $(this).closest('.card').find('.sections-container').slideToggle();
        } else {

            window.location.href = dashboardUrl + '?chapter=' + chapterId;
        }
    });


    $('.section-header').click(function(e) {
        e.preventDefault();
        const sectionId = $(this).data('id');


        if (sectionId == activeSection) {

            $(this).closest('.card').find('.subsections-container').slideToggle();

            $('.section-header').not(this).closest('.card').find('.subsections-container').slideUp();
        } else {

            window.location.href = dashboardUrl + '?chapter=' + activeChapter + '&section=' + sectionId;
        }
    });

    $('.subsection-header').click(function(e) {
        e.preventDefault();
        const subsectionId = $(this).data('id');

        if (subsectionId == activeSubsection) {

            $(this).closest('.card').find('.qa-container').slideToggle();


            $('.subsection-header').not(this).closest('.card').find('.qa-container').slideUp();
        } else {

            window.location.href = dashboardUrl + '?chapter=' + activeChapter + '&section=' + activeSection + '&subsection=' + subsectionId;
        }
    });


    $('.qa-item').click(function() {
        const qaId = $(this).data('id');

        alert('Navigate to QA item ' + qaId + ' (to be implemented)');

    });

    $('.add-chapter').click(function() {
        $('#createChapterModal').modal('show');
    });


    $('.add-section').click(function() {
        const chapterId = $(this).data('chapter');
        $('#sectionChapterId').val(chapterId);
        $('#createSectionModal').modal('show');
    });

    $('.add-subsection').click(function() {
        const sectionId = $(this).data('section');
        $('#subsectionSectionId').val(sectionId);
        $('#createSubsectionModal').modal('show');
    });

    $('.add-qa').click(function() {
        const subsectionId = $(this).data('subsection');

        alert('Navigate to QA creation for subsection ' + subsectionId + ' (to be implemented)');

    });

    $('#submitChapter').click(function() {
        const form = $('#createChapterForm');
        const formData = {
            title: $('#chapterTitle').val(),
            description: $('#chapterDescription').val(),
            order: $('#chapterOrder').val(),
            csrfmiddlewaretoken: form.find('input[name="csrfmiddlewaretoken"]').val()
        };

        $.ajax({
            url: '/chapter/create/',
            method: 'POST',
            data: formData,
            success: function(response) {
                $('#createChapterModal').modal('hide');
                window.location.reload();
            },
            error: function(xhr, status, error) {
                // Handle errors, show validation messages, etc.
                alert('Произошла ошибка при создании главы. Пожалуйста, проверьте введенные данные.');
            }
        });
    });

    // Clear form when modal is closed
    $('#createChapterModal').on('hidden.bs.modal', function () {
        $('#createChapterForm')[0].reset();
    });

    // Section creation
    $('#submitSection').click(function() {
        const form = $('#createSectionForm');
        const formData = {
            title: $('#sectionTitle').val(),
            description: $('#sectionDescription').val(),
            order: $('#sectionOrder').val(),
            chapter_id: $('#sectionChapterId').val(),
            csrfmiddlewaretoken: form.find('input[name="csrfmiddlewaretoken"]').val()
        };

        $.ajax({
            url: '/section/create/',
            method: 'POST',
            data: formData,
            success: function(response) {
                $('#createSectionModal').modal('hide');
                window.location.reload();
            },
            error: function(xhr, status, error) {
                alert('Произошла ошибка при создании раздела. Пожалуйста, проверьте введенные данные.');
            }
        });
    });

    // Subsection creation
    $('#submitSubsection').click(function() {
        const form = $('#createSubsectionForm');
        const formData = {
            title: $('#subsectionTitle').val(),
            description: $('#subsectionDescription').val(),
            order: $('#subsectionOrder').val(),
            section_id: $('#subsectionSectionId').val(),
            csrfmiddlewaretoken: form.find('input[name="csrfmiddlewaretoken"]').val()
        };

        $.ajax({
            url: '/subsection/create/',
            method: 'POST',
            data: formData,
            success: function(response) {
                $('#createSubsectionModal').modal('hide');
                window.location.reload();
            },
            error: function(xhr, status, error) {
                alert('Произошла ошибка при создании подраздела. Пожалуйста, проверьте введенные данные.');
            }
        });
    });

    // Clear forms when modals are closed
    $('#createSectionModal').on('hidden.bs.modal', function () {
        $('#createSectionForm')[0].reset();
    });

    $('#createSubsectionModal').on('hidden.bs.modal', function () {
        $('#createSubsectionForm')[0].reset();
    });
});