import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.models.slide import SlideModel
from api.models.question import QuestionModel
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Import SlideModel entries from a JSON manifest."

    def add_arguments(self, parser):
        parser.add_argument(
            "manifest_path",
            type=str,
            help="Path to the JSON manifest file on the server.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate only; do not create any SlideModel entries.",
        )

    def handle(self, *args, **options):
        manifest_path = options["manifest_path"]
        dry_run = options["dry_run"]

        if not os.path.exists(manifest_path):
            raise CommandError(f"Manifest not found: {manifest_path}")

        self.stdout.write(f"Loading manifest: {manifest_path}")
        with open(manifest_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise CommandError(f"Invalid JSON: {e}")

        if not isinstance(data, list):
            raise CommandError("Manifest root must be a list of slide entries.")

        created = 0
        skipped = 0
        errors = 0

        for idx, entry in enumerate(data, start=1):
            self.stdout.write(f"\n[{idx}] Processing entry: {entry}")

            try:
                question_id = entry["question_id"]
                accession_no = entry["accession_no"]
                slide_no = entry["slide_no"]
                description = entry.get("description", "").strip()
            except KeyError as e:
                self.stderr.write(f"  ERROR: Missing required key: {e}")
                errors += 1
                continue

            # Lookup question
            try:
                question = QuestionModel.objects.get(pk=question_id)
            except QuestionModel.DoesNotExist:
                self.stderr.write(f"  ERROR: Question id {question_id} does not exist.")
                errors += 1
                continue

            # Compute stem as model does
            base = f"{accession_no}-{slide_no}"
            stem = slugify(base)

            # Expected file locations under MEDIA_ROOT
            thumb_abs = os.path.join(settings.THUMBNAIL_ROOT, f"{stem}.jpeg")
            dzi_xml_abs = os.path.join(settings.DZI_ROOT, f"{stem}.dzi")
            dzi_tiles_abs = os.path.join(settings.DZI_ROOT, f"{stem}_files")

            if not os.path.exists(dzi_xml_abs):
                self.stderr.write(f"  ERROR: DZI XML not found: {dzi_xml_abs}")
                errors += 1
                continue

            if not os.path.isdir(dzi_tiles_abs):
                self.stderr.write(f"  WARNING: DZI tiles folder not found: {dzi_tiles_abs}")

            if not os.path.exists(thumb_abs):
                self.stderr.write(f"  WARNING: Thumbnail not found: {thumb_abs}")

            self.stdout.write(f"  OK: {accession_no} {slide_no} -> stem={stem}")
            self.stdout.write(f"  DZI XML: {dzi_xml_abs}")

            if dry_run:
                skipped += 1
                continue

            slide, created_flag = SlideModel.objects.get_or_create(
                question=question,
                accession_no=accession_no,
                slide_no=slide_no,
                defaults={
                    "description": description,
                },
            )

            # save() will recompute stem and paths, but we can call it to be safe
            slide.description = description or slide.description
            slide.save()

            self.stdout.write(f"  {'Created' if created_flag else 'Updated'} SlideModel id={slide.id}")
            if created_flag:
                created += 1

        self.stdout.write("\n=== Import complete ===")
        self.stdout.write(f"Created: {created}")
        self.stdout.write(f"Dry-run skipped: {skipped}")
        self.stdout.write(f"Errors: {errors}")