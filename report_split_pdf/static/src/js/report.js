odoo.define('report_split_pdf.report', function (require) {
"use strict";

var ActionManager = require('web.ActionManager');
var core = require('web.core');


var _t = core._t;
var _lt = core._lt;

// Messages that might be shown to the user dependening on the state of wkhtmltopdf
var link = '<br><br><a href="http://wkhtmltopdf.org/" target="_blank">wkhtmltopdf.org</a>';
var WKHTMLTOPDF_MESSAGES = {
    broken: _lt('Your installation of Wkhtmltopdf seems to be broken. The report will be shown ' +
                'in html.') + link,
    install: _lt('Unable to find Wkhtmltopdf on this system. The report will be shown in ' +
                 'html.') + link,
    upgrade: _lt('You should upgrade your version of Wkhtmltopdf to at least 0.12.0 in order to ' +
                 'get a correct display of headers and footers as well as support for ' +
                 'table-breaking between pages.') + link,
    workers: _lt('You need to start Odoo with at least two workers to print a pdf version of ' +
                 'the reports.'),
};

ActionManager.include({
    _triggerDownloadById: function (action, options, type, id){
        var self = this;
        var reportUrls = this._makeReportUrlsById(action, id);
        return this._downloadReport(reportUrls[type]).then(function () {
            if (action.close_on_report_download) {
                var closeAction = { type: 'ir.actions.act_window_close' };
                return self.doAction(closeAction, _.pick(options, 'on_close'));
            } else {
                return options.on_close();
            }
        });
    },

    _executeReportAction: function (action, options) {
        var self = this;
        if (action.report_type === 'qweb-pdf' && action.is_split_pdf) {
            // check the state of wkhtmltopdf before proceeding
            return this.call('report', 'checkWkhtmltopdf').then(function (state) {
                // display a notification according to wkhtmltopdf's state
                if (state in WKHTMLTOPDF_MESSAGES) {
                    self.do_notify(_t('Report'), WKHTMLTOPDF_MESSAGES[state], true);
                }

                if (state === 'upgrade' || state === 'ok') {
                    // trigger the download of the PDF report
                    _.each(action.context.active_ids, function (id) {
                        return self._triggerDownloadById(action, options, 'pdf', id);
                    });
                } else {
                    // open the report in the client action if generating the PDF is not possible
                    return self._executeReportClientAction(action, options);
                }
            });
        }
        return this._super.apply(this, arguments);
    },

    _makeReportUrlsById: function (action, id) {
        var reportUrls = {
            html: '/report/html/' + action.report_name,
            pdf: '/report/pdf/' + action.report_name,
            text: '/report/text/' + action.report_name,
        };
        // We may have to build a query string with `action.data`. It's the place
        // were report's using a wizard to customize the output traditionally put
        // their options.
        if (_.isUndefined(action.data) || _.isNull(action.data) ||
            (_.isObject(action.data) && _.isEmpty(action.data))) {
            var activeIDsPath = '/' + id;
            reportUrls = _.mapObject(reportUrls, function (value) {
                return value += activeIDsPath;
            });
        } else {
            var serializedOptionsPath = '?options=' + encodeURIComponent(JSON.stringify(action.data));
            serializedOptionsPath += '&context=' + encodeURIComponent(JSON.stringify(action.context));
            reportUrls = _.mapObject(reportUrls, function (value) {
                return value += serializedOptionsPath;
            });
        }
        return reportUrls;
    },
});
});
