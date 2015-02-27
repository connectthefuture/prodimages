/**
 * Created by johnb on 2/24/15.
 */
// leave at least 2 line with only a star on it below, or doc generation fails
/*
 *
 *
 */
// we want strict javascript that fails on ambiguous syntax
"using strict";

// activate extensions only after Notebook is initialized
require(["base/js/events"], function(events) {
    $([IPython.events]).on("app_initialized.NotebookApp", function() {
        /*
         * all exentensions from IPython-notebook-extensions, uncomment to activate
         */
        // PUBLISHING
        IPython.load_extensions('publishing/nbviewer_theme/main');
        //IPython.load_extensions('publishing/gist_it');
        IPython.load_extensions('publishing/nbconvert_button');
        IPython.load_extensions('publishing/printview_button');
        IPython.load_extensions('publishing/printviewmenu_button');

        // SLIDEMODE
        IPython.load_extensions('slidemode/main');


        // STYLING
        IPython.load_extensions('styling/css_selector/main');

        // TESTING
        IPython.load_extensions('testing/hierarchical_collapse/main');
        IPython.load_extensions('testing/history/history');
        IPython.load_extensions('testing/cellstate');

        // USABILITY
        IPython.load_extensions('usability/aspell/ipy-aspell');
        IPython.load_extensions('usability/codefolding/codefolding');
        IPython.load_extensions('usability/dragdrop/drag-and-drop');
        IPython.load_extensions('usability/runtools/runtools');
        IPython.load_extensions('usability/chrome_clipboard');
        IPython.load_extensions('usability/navigation-hotkeys');
        //    IPython.load_extensions('usability/shift-tab')
        IPython.load_extensions('usability/toggle_all_line_number');
        IPython.load_extensions('usability/help_panel/help_panel');
        //    IPython.load_extensions('usability/hide_input')
        IPython.load_extensions('usability/search');
        IPython.load_extensions('usability/split-combine');
        IPython.load_extensions('usability/read-only');
        IPython.load_extensions('usability/init_cell/main')
        IPython.load_extensions('usability/autosavetime')
        IPython.load_extensions('usability/autoscroll')
        IPython.load_extensions('usability/breakpoints');
        //    IPython.load_extensions('usability/clean_start')
        IPython.load_extensions('usability/comment-uncomment')
        IPython.load_extensions('usability/linenumbers')
        //    IPython.load_extensions('usability/no_exec_dunder')
        //    IPython.load_extensions('usability/noscroll')
        //    IPython.load_extensions('usability/hide_io_selected')
        IPython.load_extensions('usability/execute_time/ExecuteTime');
        IPython.load_extensions('usability/python-markdown')
    });
});
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
//////      END Ipython Extentions Loading /////////////////
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
////// Example from IPython install at top commented out ///
// $([IPython.events]).on('app_initialized.NotebookApp', function () {
//     IPython.toolbar.add_buttons_group([
//         {
//             'label': 'run qtconsole',
//             'icon': 'icon-terminal', // select your icon from http://fortawesome.github.io/Font-Awesome/icons
//             'callback': function () {
//                 IPython.notebook.kernel.execute('%qtconsole')
//             }
//         }
//         // add more button here if needed.
//     ]);
// }));