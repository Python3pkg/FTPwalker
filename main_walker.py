from multiprocessing import Pool
from traverse import Run
from datetime import datetime
import json
from collections import OrderedDict
from os import path as ospath, listdir
import csv


class main_walker:
    def __init__(self, *args, **kwargs):
        self.server_name = kwargs['server_name']
        self.url = kwargs['url']
        self.root = kwargs['root']
        self.server_path = kwargs['server_path']

    def Process_dispatcher(self, resume):
        run = Run(self.server_name,
                  self.url,
                  self.root,
                  self.server_path,
                  resume)
        base, leadings = run.find_leading(self.root, thread_flag=False)
        path, _ = base[0]
        leadings = [ospath.join(path, i.strip('/')) for i in leadings]
        print ("Root's leadings are: ", leadings)

        all_leadings = run.find_all_leadings(leadings)
        lenght_of_subdirectories = sum(len(dirs) for _, (_, dirs) in all_leadings.items())
        print("{} subdirectories founded".format(lenght_of_subdirectories))
        try:
            pool = Pool()
            pool.map(run.main_run, all_leadings.items())
        except Exception as exp:
            print(exp)
        else:
            print ('***' * 5, datetime.now(), '***' * 5)
            file_names = listdir(self.server_path)
            if lenght_of_subdirectories == len(file_names):
                main_dict = OrderedDict()
                for name in file_names:
                    with open(ospath.join(self.server_path, name)) as f:
                        csvreader = csv.reader(f)
                        for path_, *files in csvreader:
                            main_dict[path_] = files
                self.create_json(main_dict, self.server_name)
            else:
                print("Traversing isn't complete. Start resuming the {} server...".format(self.name))
                self.Process_dispatcher(True)

    def create_json(self, dictionary, name):
        # json_path = ospath.join(*ospath.dirname(__file__).split('/')[:-1].__add__(
        #    ['database/json_files/{}.json'.format(name)]))
        with open('{}.json'.format(name), 'w') as fp:
            json.dump(dictionary, fp, indent=4)