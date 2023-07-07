from django.core.management import BaseCommand
from sprocket.models import Factory, Sprocket, SprocketProduction
from datetime import datetime, timezone
from django.db import IntegrityError
from django.db import transaction


class Command(BaseCommand):
    help = (
        "Build factory and sprocket data based on json sent through the documentation"
    )

    @staticmethod
    def get_json_data():
        from sprocket.utils.utils import read_json_file

        factory_json = read_json_file("sprocket/fixtures/seed_factory_data.json")
        sprockets_json = read_json_file("sprocket/fixtures/seed_sprocket_types.json")
        return factory_json, sprockets_json

    def handle(self, *args, **kwargs):
        factory_json, sprockets_json = self.get_json_data()
        sprockets_factory = []
        with transaction.atomic():
            try:
                for index, sprocket in enumerate(sprockets_json["sprockets"]):
                    sprocket_obj = Sprocket(
                        date_created=datetime.now(timezone.utc),
                        **sprocket,
                    )

                    chart_data = factory_json["factories"][index]["factory"][
                        "chart_data"
                    ]
                    production_amount = len(chart_data["sprocket_production_actual"])

                    factory_obj = Factory(
                        date_created=datetime.now(timezone.utc),
                        name=f"Factory {index+1}",
                        sprocket_actual=chart_data["sprocket_production_actual"][
                            production_amount - 1
                        ],
                        sprocket_goal=chart_data["sprocket_production_goal"][
                            production_amount - 1
                        ],
                    )

                    sprocket_obj.save()
                    factory_obj.save()

                    for prod_index in range(production_amount):
                        sprocket_production_payload = {
                            "sprocket": sprocket_obj,
                            "factory": factory_obj,
                            "sprocket_actual": chart_data["sprocket_production_actual"][
                                prod_index
                            ],
                            "sprocket_goal": chart_data["sprocket_production_goal"][
                                prod_index
                            ],
                            "date_created": datetime.now(timezone.utc),
                            "date_produced": datetime.fromtimestamp(
                                int(chart_data["time"][prod_index]), timezone.utc
                            ),
                        }
                        sprocketProduction = SprocketProduction(
                            **sprocket_production_payload
                        )
                        sprocketProduction.save()
                        sprockets_factory.append(sprocketProduction)

                self.stderr.write(
                    self.style.SUCCESS(
                        "Factory and sprocket data generated successfully"
                    )
                )
            except IntegrityError as e:
                transaction.set_rollback(True)
                error_message = f"Check the data you are sending through: {str(e)}"
                self.stderr.write(self.style.ERROR(error_message))
                raise
