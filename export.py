import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server, Info
from jtop import jtop

class CustomCollector(object):
    def __init__(self,Jetson):
        self.jetson = Jetson
        pass

    def __cpu(self):
        cpu_gauge = GaugeMetricFamily(
            'cpu', 'cpu statistics from tegrastats', labels=['core', 'statistic'],
        )
        for core_number,core_data  in self.jetson.cpu.items():
            cpu_gauge.add_metric([core_number, 'freq'], value=core_data['frq'])
            cpu_gauge.add_metric([core_number, 'val'], value=core_data['val'])
            cpu_gauge.add_metric([core_number, 'min_freq'], value=core_data['min_freq']) 
            cpu_gauge.add_metric([core_number, 'max_freq'], value=core_data['max_freq'])             
        return cpu_gauge

    def __gpu(self):
        gpu_gauge = GaugeMetricFamily(
            'gpu_utilization_percentage', 'gpu statistics from tegrastats',
        )
        gpu_gauge.add_metric([], value=str(self.jetson.gpu['val']))
        return gpu_gauge

    def __ram(self):
        ram_gauge = GaugeMetricFamily(
            'ram',f'ram statistics from tegrastats ',labels=['statistic'],
        )
        ram_gauge.add_metric(['total'], value=self.jetson.ram['tot'])
        ram_gauge.add_metric(['used'], value=self.jetson.ram['use'])
        ram_gauge.add_metric(['CPU_used'], value=self.jetson.ram['use']-self.jetson.ram['shared'])
        ram_gauge.add_metric(['GPU_used'], value=self.jetson.ram['shared'])
        return ram_gauge

    def __temperature(self):
        temperature_gauge = GaugeMetricFamily(
            'temperature', 'temperature statistics from tegrastats',labels=['machine_part'],
        )
        for machine_part, temperature in self.jetson.temperature.items():
            temperature_gauge.add_metric([machine_part], value=str(temperature))
        return temperature_gauge

    def __voltage(self):
        voltage_gauge = GaugeMetricFamily(
            'mWatt', 'mWatt statistics from tegrastats', labels=['source'],
        )
        voltage_gauge.add_metric(['cur'], value=str(self.jetson.power[0]['cur']))
        voltage_gauge.add_metric(['avg'], value=str(self.jetson.power[0]['avg']))
        return voltage_gauge

    def __nvpmodel(self):
        nvpmodel_gauge = GaugeMetricFamily('nvpmodel', 'NV Power Model',labels=['nvpmodel'],)
        nvpmodel_gauge.add_metric([str(self.jetson.nvpmodel)], value=0)
        return nvpmodel_gauge

    def __emc(self):
        emc_gauge = GaugeMetricFamily(
            'emc','emc statistics from tegrastats', labels=['statistic'],
        )
        emc_gauge.add_metric(['val'], value=self.jetson.emc['val'])
        emc_gauge.add_metric(['frq'], value=self.jetson.emc['frq'])
        emc_gauge.add_metric(['min_freq'], value=self.jetson.emc['min_freq'])
        emc_gauge.add_metric(['max_freq'], value=self.jetson.emc['max_freq'])
        return emc_gauge

    def collect(self):
        yield self.__cpu()
        yield self.__gpu()
        yield self.__ram()
        yield self.__temperature()
        yield self.__voltage()
        yield self.__nvpmodel()
        yield self.__emc()
        yield self.__info()
        yield self.__hardware()

def info_jetson(jetson):
    i = Info('info', 'Description of info')
    i.info(jetson.board['info'])

def hardware_jetson(jetson):
    i = Info('hardware', 'Description of hardware')
    i.info(jetson.board['hardware'])    

def libraries_jetson(jetson):
    i = Info('libraries', 'Description of libraries')
    i.info(jetson.board['libraries'])   

if __name__ == '__main__':
    start_http_server(8001)
    with jtop() as jetson:
        info_jetson(jetson)
        hardware_jetson(jetson)
        libraries_jetson(jetson)
        REGISTRY.register(CustomCollector(jetson))
        while True:
            time.sleep(1)

