from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Prefetch
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from ..monitorings.models import Monitoring, MonitoringInstitution


class QuestionQuerySet(models.QuerySet):
    pass


# TODO: Make registers to dynamically

@python_2_unicode_compatible
class Question(TimeStampedModel):
    TYPE = Choices(('short_text', _('Short text answer')),
                   ('long_text', _('Long text answer')),
                   ('choice', _("Choice answer")))
    monitoring = models.ForeignKey(to=Monitoring,
                                   verbose_name=_("Monitoring"))
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                   verbose_name=_("Created by"))
    name = models.CharField(verbose_name=_("Title"),
                            max_length=100)
    description = models.TextField(verbose_name=_("Description"),
                                   blank=True)
    type = models.CharField(choices=TYPE,
                            default=TYPE.short_text,
                            verbose_name=_("Answer type"),
                            max_length=25)
    order = models.PositiveSmallIntegerField(verbose_name=_("Order"))
    count = JSONField(blank=True)
    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['order', 'created', ]

    def __str__(self):
        return self.name


class ChoiceQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Choice(TimeStampedModel):
    question = models.ForeignKey(to=Question,
                                 verbose_name=_("Question"),
                                 limit_choices_to={'type': Question.TYPE.choice})
    key = models.CharField(max_length=50, verbose_name=_("Key"))
    value = models.CharField(max_length=50, verbose_name=_("Value"))
    order = models.PositiveSmallIntegerField(verbose_name=_("Order"))

    objects = ChoiceQuerySet.as_manager()

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")
        ordering = ['order', 'created', ]
        unique_together = (("question", "key"),)

    def __str__(self):
        return self.value


class ConditionQuerySet(models.QuerySet):
    pass


class Condition(TimeStampedModel):
    TYPE = Choices(('is-true', _('Is true')),
                   ('is-false', _('Is false')),
                   ('is-equal', _("Is equal")),
                   ('is-not-equal', _("Is not equal")),
                   ('is-less', _('Is less')),
                   ('is-more', _('Is more'))
                   )
    type = models.CharField(choices=TYPE,
                            default='is-true',
                            max_length=15,
                            verbose_name=_("Answer type"))
    target = models.ForeignKey(to=Question,
                               related_name="condition_target",
                               null=True,
                               blank=True,
                               verbose_name=_("Target"))
    related = models.ForeignKey(to=Question,
                                related_name="condition_related",
                                verbose_name=_("Related"))
    value = models.CharField(max_length=50,
                             verbose_name=_("Value"),
                             blank=True)
    objects = ConditionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Condition")
        verbose_name_plural = _("Conditions")
        ordering = ['created', ]


class SheetQuerySet(models.QuerySet):
    def monitoring(self, monitoring):
        return self.filter(monitoring_institution__monitoring=monitoring)

    def institution(self, institution):
        return self.filter(monitoring_institution__institution=institution)

    def with_answer(self):
        qs = self.prefetch_related('answer_set',
                                   'answer_set__answertext')
        prefetch = Prefetch('answer_set__answerchoice',
                            queryset=AnswerChoice.objects.select_related('value'))
        return qs.prefetch_related(prefetch)


class Sheet(TimeStampedModel):
    monitoring_institution = models.ForeignKey(to=MonitoringInstitution)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             verbose_name=_("User"))
    point = models.IntegerField(verbose_name=_("Point"))
    objects = SheetQuerySet.as_manager()

    @property
    def monitoring(self):
        return self.monitoring_institution.monitoring

    @property
    def institution(self):
        return self.monitoring_institution.institution

    def get_sheet_url(self):
        return reverse('monitorings:sheet_list', kwargs={'slug': self.monitoring.slug,
                                                         'institution_slug': self.institution.slug})

    class Meta:
        verbose_name = _("Sheet")
        verbose_name_plural = _("Sheets")
        ordering = ['monitoring_institution', 'user', 'created', ]
        unique_together = (("monitoring_institution", "user"),)


class AnswerQuerySet(models.QuerySet):
    pass


class Answer(TimeStampedModel):
    question = models.ForeignKey(to=Question,
                                 verbose_name=_("Question"))
    sheet = models.ForeignKey(to=Sheet,
                              verbose_name=_("Sheet"))
    objects = AnswerQuerySet.as_manager()

    def type(self):
        if self.answertext:
            return 1
        if self.answerchoice:
            return 2

    @property
    def has_answerchoice(self):
        try:
            self.answerchoice
            return True
        except AnswerChoice.DoesNotExist:
            return False

    @property
    def has_answertext(self):
        try:
            self.answertext
            return True
        except AnswerText.DoesNotExist:
            return False

    def value(self):
        if self.has_answertext:
            return self.answertext.value or '-'
        if self.has_answerchoice:
            return self.answerchoice.value or '-'
        return '-'

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        unique_together = (("question", "sheet"),)


class AbstractAnswerTypeQuerySet(models.QuerySet):
    pass


class AbstractAnswerType(TimeStampedModel):
    answer = models.OneToOneField(Answer)
    objects = AbstractAnswerTypeQuerySet.as_manager()

    class Meta:
        abstract = True


class AnswerTextQuerySet(AbstractAnswerTypeQuerySet):
    pass


class AnswerText(AbstractAnswerType):
    value = models.CharField(verbose_name=_("Value"), blank=True, max_length=150)
    objects = AnswerTextQuerySet.as_manager()

    class Meta:
        verbose_name = _("Text answer")
        verbose_name_plural = _("Text answers")


class AnswerChoiceQuerySet(AbstractAnswerTypeQuerySet):
    pass


class AnswerChoice(AbstractAnswerType):
    value = models.ForeignKey(Choice, verbose_name=_("Value"))
    objects = AnswerChoiceQuerySet.as_manager()

    class Meta:
        verbose_name = _("Choice answer")
        verbose_name_plural = _("Choice answers")
