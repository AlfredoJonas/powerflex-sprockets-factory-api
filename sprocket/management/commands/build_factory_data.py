from django.core.management import BaseCommand
from sprocket.models import Factory, Sprocket, SprocketProduction
from sprocket.utils.utils import read_json_file
from datetime import datetime, timezone

class Command(BaseCommand):
    help = "Build factory and sprocket data based on json sent through the documentation"

    def handle(self, *args, **kwargs):
        sprockets_json = read_json_file("sprocket/fixtures/seed_sprocket_types.json")
        factory_json = read_json_file("sprocket/fixtures/seed_factory_data.json")
        try:
            for index, sprocket in enumerate(sprockets_json['sprockets']):
                sprocket_obj = Sprocket(id=index+1, date_created=datetime.now(timezone.utc), **sprocket)
                factory_obj = Factory(id=index+1, date_created=datetime.now(timezone.utc), name=f"Factory {index+1}")
                sprocket_obj.save()
                factory_obj.save()
                chart_data = factory_json['factories'][index]['factory']['chart_data']
                production_amount = len(chart_data['sprocket_production_actual'])
                for prod_index in range(production_amount):
                    sprocket_production_payload = {
                        "sprocket": sprocket_obj,
                        "factory": factory_obj,
                        "sprocket_actual": chart_data['sprocket_production_actual'][prod_index],
                        "sprocket_goal": chart_data['sprocket_production_goal'][prod_index],
                        "date_created": datetime.now(timezone.utc),
                        "date_produced": datetime.fromtimestamp(int(chart_data['time'][prod_index]), timezone.utc)
                    }
                    sprocketProduction = SprocketProduction(**sprocket_production_payload)
                    sprocketProduction.save()
            
            self.stderr.write(self.style.SUCCESS("Factory and sprocket data generated successfully"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Something bad happens: {str(e)}"))

