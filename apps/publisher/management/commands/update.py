from django.core.management import BaseCommand
from publisher.models import Experiment, Frequency, Project
from scripts.updated_values import replaced_frequencies, \
                                   removed_frequencies, \
                                   replaced_experiments, \
                                   removed_experiments


class Command(BaseCommand):
    help = "Update the values of project facets with new ones."

    def handle(self, *args, **options):

        # Frequencies
        print('replacing publication frequencies')
        for project_name, frequencies in replaced_frequencies.items():
            project = Project.objects.filter(project=project_name)[0]
            publications = Project.objects.get(project__iexact=project_name).publication_set
            for old_freq, new_freq in frequencies.items():
                # Add new frequency if not already in the table
                if not Frequency.objects.filter(frequency=new_freq).exists():
                    new_frequency = Frequency(frequency=new_freq)
                    new_frequency.save()
                # Add new frequency if not already in the project
                if not project.frequencies.filter(frequency=new_freq).exists():
                    project.frequencies.add(Frequency.objects.filter(frequency=new_freq)[0])
                # Replace old frequency in publications with new one
                if Frequency.objects.filter(frequency=old_freq).exists():
                    old_frequency = Frequency.objects.filter(frequency=old_freq)
                    for pub in publications.filter(frequency=old_frequency[0]):
                        pub.frequency.add(Frequency.objects.filter(frequency=new_freq)[0])
                        pub.frequency.filter(frequency=old_freq).delete()
        print('deleting old frequencies')
        # Remove old frequencies from table
        for old_freq in removed_frequencies:
            if Frequency.objects.filter(frequency=old_freq).exists():
                Frequency.objects.filter(frequency=old_freq).delete()
        print('frequencies done')

        # Experiments
        print('replacing publication experiments')
        for project_name, experiments in replaced_experiments.items():
            project = Project.objects.filter(project=project_name)[0]
            publications = Project.objects.get(project__iexact=project_name).publication_set
            for old_exp, new_exp in experiments.items():
                # Add new experiment if not already in the table
                if not Experiment.objects.filter(experiment=new_exp).exists():
                    new_experiment = Experiment(experiment=new_exp)
                    new_experiment.save()
                # Add new experiment if not already in the project
                if not project.experiments.filter(experiment=new_exp).exists():
                    project.experiments.add(Experiment.objects.filter(experiment=new_exp)[0])
                # Replace old experiment in publications with new one
                if Experiment.objects.filter(experiment=old_exp).exists():
                    old_experiment = Experiment.objects.filter(experiment=old_exp)
                    for pub in publications.filter(experiments=old_experiment[0]):
                        pub.experiments.add(Experiment.objects.filter(experiment=new_exp)[0])
                        pub.experiments.filter(experiment=old_exp).delete()
        print('deleting old experiments')
        # Remove old experiments from table
        for old_exp in removed_experiments:
            if Experiment.objects.filter(experiment=old_exp).exists():
                Experiment.objects.filter(experiment=old_exp).delete()
        print('experiments done')
