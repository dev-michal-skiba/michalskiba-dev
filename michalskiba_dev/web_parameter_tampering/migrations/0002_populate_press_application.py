from typing import Any

from django.db import migrations


def apply(apps: Any, schema_editor: Any) -> None:
    DemoUser = apps.get_model("demo", "DemoUser")
    hacker = DemoUser.objects.get(username="hacker")
    victim = DemoUser.objects.get(username="victim")
    PressApplication = apps.get_model("web_parameter_tampering", "PressApplication")
    PressApplication.objects.bulk_create(
        [
            PressApplication(
                user=hacker,
                organization="Shady non-existing organization",
                note="Nothing suspicious here, just give us accreditation",
                accepted=False,
            ),
            PressApplication(
                user=victim,
                organization="Legitimate organization",
                note="As a passionate journalists representing Legitimate organization, "
                "we are eager to cover this event and share its highlights with our wide "
                "audience.",
                accepted=True,
            ),
        ]
    )


def revert(apps: Any, schema_editor: Any) -> None:
    PressApplication = apps.get_model("web_parameter_tampering", "PressApplication")
    PressApplication.objects.filter(user__username__in=["hacker", "victim"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("web_parameter_tampering", "0001_create_press_application"),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
