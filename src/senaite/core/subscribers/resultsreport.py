# -*- coding: utf-8 -*-

from datetime import datetime
from zope.component import adapter, getUtility
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from plone.registry.interfaces import IRegistry

from senaite.core.interfaces import IResultsReport
from senaite.core import logger


@adapter(IResultsReport, IAfterTransitionEvent)
def resultsreport_after_publish(report, event):
    # Só no publish
    if not event.transition or event.transition.id != "publish":
        return

    # Se já tem número, não gera de novo
    if report.getField("report_number").get(report):
        return

    number = generate_report_number()

    report.getField("issue_date").set(report, datetime.now())
    report.getField("report_number").set(report, number)
    report.getField("report_revision").set(report, u"00")

    report.reindexObject(idxs=[
        "report_number",
        "report_revision",
        "issue_date",
    ])

    logger.info(
        "ResultsReport %s published with number %s",
        report.getId(),
        number,
    )
