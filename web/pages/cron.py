from django.core.management import call_command

# class DatabaseUpdateJob(CronJobBase):
#     RUN_AT_TIMES = ['4:00', '12:21']

#     schedule = Schedule(run_at_times=RUN_AT_TIMES)
#     code = 'pages.update'

#     def do(self):
#         call_command('fetchdata') 

# class TestJob(CronJobBase):
#     RUN_EVERY_MINS = 1

#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'pages.test'

#     def do(self):
#         print("The task is running!")

# def test_job():
#     print("The task is running!")