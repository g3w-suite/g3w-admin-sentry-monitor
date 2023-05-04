from django.conf import settings
from django.apps import AppConfig

from base.version import get_version


class SentryMonitorConfig(AppConfig):
    name = 'sentry_monitor'
    verbose_name = "Sentry Monitor"

    ##
    # Python integration: https://docs.sentry.io/platforms/python/
    ##
    if ( hasattr(settings, 'SENTRY_PY_DSN') ):
        import sentry_sdk

        sentry_sdk.init(

            # A DSN tells a Sentry SDK where to send events 
            # so the events are associated with the correct project.
            dsn = settings.SENTRY_PY_DSN,

            release = "g3w-admin@" + get_version(),

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,

        )

    ##
    # Javascript integration: https://docs.sentry.io/platforms/javascript/
    ##
    if ( hasattr(settings, 'SENTRY_JS_DSN') ):

        settings.SENTRY_JS = """
        <script src="https://browser.sentry-cdn.com/7.31.0/bundle.tracing.min.js" integrity="sha384-g/zdHeV5+PqD7HmWeWVuK9wYkqRN+1NlqveOyyditZgHVahR/Et3SFTLepAHqQyo" crossorigin="anonymous"></script>
        <script>
            if (Sentry) {
            Sentry.init({

                /**
                * A DSN tells a Sentry SDK where to send events so the events
                * are associated with the correct project.
                *
                * @see https://docs.sentry.io/product/sentry-basics/dsn-explainer/
                */
                dsn: "{{SENTRY_JS_DSN}}",

                /**
                * Alternatively, use `process.env.npm_package_version`
                * for a dynamic release version if your build tool
                * supports it.
                */
                release: "g3w-admin@{{version}}",

                integrations: [new Sentry.BrowserTracing()],

                /**
                * Set tracesSampleRate to 1.0 to capture 100%
                * of transactions for performance monitoring.
                * We recommend adjusting this value in production
                */
                tracesSampleRate: 1.0,

                /**
                * Check if it is an exception, and if so,
                * show the report dialog
                */
                beforeSend(event, hint) {
                    if (event.exception && !["localhost", "127.0.0.1"].includes(location.hostname)) {
                        Sentry.showReportDialog({ eventId: event.event_id, lang: 'it' });
                    }
                    return event;
                },

            });
            }
        </script>
        """.replace("{{version}}", get_version()).replace("{{SENTRY_JS_DSN}}", settings.SENTRY_JS_DSN)
