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

    // Only sho active items based on URL parameters
    if (activeChapter) {
        $('[data-id="' + activeChapter + '"]').closest('.card').find('.sections-container').show();
    }

    if (activeSection) {
        $('[data-id="' + activeSection + '"]').closest('.card').find('.subsections-container').show();
    }

    if (activeSubsection) {
        $('[data-id="' + activeSubsection + '"]').closest('.card').find('.qa-container').show();
    }

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

        alert('Navigate to chapter creation (to be implemented)');

    });


    $('.add-section').click(function() {
        const chapterId = $(this).data('chapter');

        alert('Navigate to section creation for chapter ' + chapterId + ' (to be implemented)');

    });

    $('.add-subsection').click(function() {
        const sectionId = $(this).data('section');

        alert('Navigate to subsection creation for section ' + sectionId + ' (to be implemented)');

    });

    $('.add-qa').click(function() {
        const subsectionId = $(this).data('subsection');

        alert('Navigate to QA creation for subsection ' + subsectionId + ' (to be implemented)');

    });
});