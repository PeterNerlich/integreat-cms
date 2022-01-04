import logging

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .abstract_base_page_translation import AbstractBasePageTranslation
from .page import Page


logger = logging.getLogger(__name__)


class PageTranslation(AbstractBasePageTranslation):
    """
    Data model representing a page translation
    """

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name=_("page"),
    )
    text = models.TextField(
        blank=True,
        verbose_name=_("content of the page"),
    )

    @property
    def ancestor_path(self):
        """
        This property calculates the path of all parents of the page

        :return: The relative path to the page
        :rtype: str
        """
        return "/".join(
            [
                ancestor.get_translation(self.language.slug).slug
                if ancestor.get_translation(self.language.slug)
                else ancestor.default_translation.slug
                for ancestor in self.page.get_ancestors()
            ]
        )

    @property
    def url_infix(self):
        """
        Generates the infix of the url of the page translation object which is the ancestor path of the page

        For information about the components of such an url,
        see :meth:`~integreat_cms.cms.models.abstract_content_translation.AbstractContentTranslation.get_absolute_url`

        :return: the infix of the url
        :rtype: str
        """
        return self.ancestor_path

    @property
    def backend_edit_link(self):
        """
        This function returns the absolute url to the editor for this translation

        :return: The url
        :rtype: str
        """
        return reverse(
            "edit_page",
            kwargs={
                "page_id": self.page.id,
                "language_slug": self.language.slug,
                "region_slug": self.page.region.slug,
            },
        )

    @property
    def short_url(self):
        """
        This function returns the absolute short url to the page translation

        :return: The short url of a page translation
        :rtype: str
        """

        return settings.BASE_URL + reverse(
            "expand_page_translation_id", kwargs={"short_url_id": self.id}
        )

    @property
    def combined_text(self):
        """
        This function combines the text from this PageTranslation with the text from the mirrored page.
        Mirrored content always includes the live content from another page. This content needs to be added when
        delivering content to end users.

        :return: The combined content of this page and the mirrored page
        :rtype: str
        """
        mirrored_page_translation = self.page.get_mirrored_page_translation(
            self.language.slug
        )
        if not mirrored_page_translation or not mirrored_page_translation.text:
            return self.text
        if self.page.mirrored_page_first:
            return mirrored_page_translation.text + self.text
        return self.text + mirrored_page_translation.text

    @property
    def combined_last_updated(self):
        """
        This function combines the last_updated date from this PageTranslation and from a mirrored page.
        If this translation has no content, then the date from the mirrored translation will be used. In
        other cases, the date from this translation will be used.

        :return: The last_updated date of this or the mirrored page translation
        :rtype: ~datetime.datetime
        """
        mirrored_page_translation = self.page.get_mirrored_page_translation(
            self.language.slug
        )
        if (
            not self.text
            and mirrored_page_translation
            and mirrored_page_translation.text
        ):
            return mirrored_page_translation.last_updated
        return self.last_updated

    @property
    def tags(self):
        """
        This functions returns a list of translated tags which apply to this function.
        Supported tags:
        * Live content: if the page of this translation has live content
        * Empty: if the page contains no text

        :return: A list of tags which apply to this translation
        :rtype: list [ str ]
        """
        tags = []

        if self.page.mirrored_page:
            tags.append(_("Live content"))

        if not self.combined_text.strip():
            tags.append(_("Empty"))

        return tags

    @classmethod
    def get_translations(cls, region, language):
        """
        This function retrieves the most recent versions of a all :class:`~integreat_cms.cms.models.pages.page_translation.PageTranslation`
        objects of a :class:`~integreat_cms.cms.models.regions.region.Region` in a specific :class:`~integreat_cms.cms.models.languages.language.Language`

        :param region: The requested :class:`~integreat_cms.cms.models.regions.region.Region`
        :type region: ~integreat_cms.cms.models.regions.region.Region

        :param language: The requested :class:`~integreat_cms.cms.models.languages.language.Language`
        :type language: ~integreat_cms.cms.models.languages.language.Language

        :return: A :class:`~django.db.models.query.QuerySet` of all page translations of a region in a specific language
        :rtype: ~django.db.models.query.QuerySet
        """
        return cls.objects.filter(page__region=region, language=language).distinct(
            "page"
        )

    @classmethod
    def get_up_to_date_translations(cls, region, language):
        """
        This function is similar to :func:`~integreat_cms.cms.models.pages.page_translation.PageTranslation.get_translations` but
        returns only page translations which are up to date

        :param region: The requested :class:`~integreat_cms.cms.models.regions.region.Region`
        :type region: ~integreat_cms.cms.models.regions.region.Region

        :param language: The requested :class:`~integreat_cms.cms.models.languages.language.Language`
        :type language: ~integreat_cms.cms.models.languages.language.Language

        :return: All up to date translations of a region in a specific language
        :rtype: list [ ~integreat_cms.cms.models.pages.page_translation.PageTranslation ]
        """
        return [
            t
            for t in cls.objects.filter(
                page__region=region, language=language
            ).distinct("page")
            if t.is_up_to_date
        ]

    @classmethod
    def get_current_translations(cls, region, language):
        """
        This function is similar to :func:`~integreat_cms.cms.models.pages.page_translation.PageTranslation.get_translations` but
        returns only page translations which are currently being translated by an external translator

        :param region: The requested :class:`~integreat_cms.cms.models.regions.region.Region`
        :type region: ~integreat_cms.cms.models.regions.region.Region

        :param language: The requested :class:`~integreat_cms.cms.models.languages.language.Language`
        :type language: ~integreat_cms.cms.models.languages.language.Language

        :return: All currently translated translations of a region in a specific language
        :rtype: list [ ~integreat_cms.cms.models.pages.page_translation.PageTranslation ]
        """
        return [
            t
            for t in cls.objects.filter(
                page__region=region, language=language
            ).distinct("page")
            if t.currently_in_translation
        ]

    @classmethod
    def get_outdated_translations(cls, region, language):
        """
        This function is similar to :func:`~integreat_cms.cms.models.pages.page_translation.PageTranslation.get_translations` but
        returns only page translations which are outdated

        :param region: The requested :class:`~integreat_cms.cms.models.regions.region.Region`
        :type region: ~integreat_cms.cms.models.regions.region.Region

        :param language: The requested :class:`~integreat_cms.cms.models.languages.language.Language`
        :type language: ~integreat_cms.cms.models.languages.language.Language

        :return: All outdated translations of a region in a specific language
        :rtype: list [ ~integreat_cms.cms.models.pages.page_translation.PageTranslation ]
        """
        return [
            t
            for t in cls.objects.filter(
                page__region=region, language=language
            ).distinct("page")
            if t.is_outdated
        ]

    class Meta:
        #: The verbose name of the model
        verbose_name = _("page translation")
        #: The plural verbose name of the model
        verbose_name_plural = _("page translations")
        #: The name that will be used by default for the relation from a related object back to this one
        default_related_name = "page_translations"
        #: The default permissions for this model
        default_permissions = ()
        #: The fields which are used to sort the returned objects of a QuerySet
        ordering = ["page__pk", "-version"]
