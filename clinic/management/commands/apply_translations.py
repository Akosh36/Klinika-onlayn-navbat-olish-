from django.core.management.base import BaseCommand
import json
import os

from clinic.models import Clinic, Doctor


class Command(BaseCommand):
    help = 'Apply translations from translations/uz.json to DB (preview by default).'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Apply changes to database')
        parser.add_argument('--file', type=str, default='translations/uz.json', help='Path to translations JSON')

    def handle(self, *args, **options):
        path = options['file']
        apply_changes = options['apply']

        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'Translation file not found: {path}'))
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # data format example:
        # {"Clinic": [{"id":1, "name":"...", "description":"...", "address":"..."}], "Doctor": [{"id":1, "name":"...", "specialty":"..."}]}

        # Process clinics
        clinics = data.get('Clinic', [])
        for entry in clinics:
            obj = None
            if 'id' in entry:
                try:
                    obj = Clinic.objects.get(pk=entry['id'])
                except Clinic.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Clinic id={entry['id']} not found"))
                    continue
            elif 'name' in entry:
                try:
                    obj = Clinic.objects.get(name=entry['name_match']) if entry.get('name_match') else Clinic.objects.get(name=entry['name'])
                except Clinic.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Clinic name match not found: {entry.get('name') or entry.get('name_match')}"))
                    continue

            changes = {}
            for field in ('name', 'description', 'address'):
                if field in entry:
                    current = getattr(obj, field)
                    new = entry[field]
                    if current != new:
                        changes[field] = (current, new)

            if not changes:
                self.stdout.write(self.style.NOTICE(f'Clinic id={obj.id} no changes'))
                continue

            self.stdout.write(self.style.MIGRATE_HEADING(f'Clinic id={obj.id} preview'))
            for k, (old, new) in changes.items():
                self.stdout.write(f' - {k}: "{old}" -> "{new}"')

            if apply_changes:
                for k, (_, new) in changes.items():
                    setattr(obj, k, new)
                obj.save()
                self.stdout.write(self.style.SUCCESS(f'Clinic id={obj.id} updated'))

        # Process doctors
        doctors = data.get('Doctor', [])
        for entry in doctors:
            obj = None
            if 'id' in entry:
                try:
                    obj = Doctor.objects.get(pk=entry['id'])
                except Doctor.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Doctor id={entry['id']} not found"))
                    continue
            elif 'name' in entry:
                name_to_match = entry.get('name_match') or entry['name']
                qs = Doctor.objects.filter(name=name_to_match)
                if not qs.exists():
                    self.stdout.write(self.style.WARNING(f"Doctor name match not found: {name_to_match}"))
                    continue
                # if multiple doctors match, update all
                objs = list(qs)


            # support updating multiple matched doctor objects
            target_objs = objs if 'objs' in locals() else [obj]
            any_changes = False
            for target in target_objs:
                changes = {}
                for field in ('name', 'specialty'):
                    if field in entry:
                        current = getattr(target, field)
                        new = entry[field]
                        if current != new:
                            changes[field] = (current, new)

                if not changes:
                    self.stdout.write(self.style.NOTICE(f'Doctor id={target.id} no changes'))
                    continue

                any_changes = True
                self.stdout.write(self.style.MIGRATE_HEADING(f'Doctor id={target.id} preview'))
                for k, (old, new) in changes.items():
                    self.stdout.write(f' - {k}: "{old}" -> "{new}"')

                if apply_changes:
                    for k, (_, new) in changes.items():
                        setattr(target, k, new)
                    target.save()
                    self.stdout.write(self.style.SUCCESS(f'Doctor id={target.id} updated'))

            if not any_changes:
                # nothing changed for any matched doctors
                pass

        self.stdout.write(self.style.NOTICE('Done. Use --apply to persist changes.'))
