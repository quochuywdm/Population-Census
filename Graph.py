import matplotlib.pyplot as plt
import seaborn as sb
import os
import cv2


class Graph:
    '''
        an Object of this Class could save Graphs into Images and render Video from saved Images
    '''
    def __init__(self, dataReader, yearsDict, imageOutputFolder, videoOutputFolder):
        self.dataReader = dataReader
        self.yearsDict = yearsDict
        self.NumberOfYears = dataReader.getCountOfYears()
        self.MaxPopulationPerCountry = dataReader.getHighestPopulationOfAllCountries()
        self.numberOfCountries = dataReader.amountOfTopCountries
        self.imageOutputFolder = imageOutputFolder
        self.videoOutputFolder = videoOutputFolder

    def render(self):
        process = 0
        for x in range(self.NumberOfYears):                         # Each loop for a year
            # Variable declaration for each year
            process = self.showLoading(process, x)                  # To show rendering process
            thisYearInt = self.dataReader.getFirstYear() + x
            thisYearObject = self.yearsDict.get(thisYearInt)
            topCountriesThisYearList = thisYearObject.getTopNameList()
            topPopulationThisYearList = thisYearObject.getTopPopulationList()

            # Size of the Image width x height in Inches
            plt.figure(figsize=(15, 10))
            # set Style in Seabron
            sb.set_style('dark')
            # Draw the Graph
            sb.barplot(
                x=topPopulationThisYearList,
                y=topCountriesThisYearList,
                palette=sb.color_palette("YlOrRd_r", self.numberOfCountries))           # Color for the bars
            # Set title
            title = "Top 20 Countries with the Highest Population".upper() + '\n ' + str(thisYearInt)
            title_obj = plt.title(title)
            plt.setp(title_obj, color='orangered', fontsize=30)

            # Draw the Axes
            plt.tick_params(axis="y",
                            labelsize=self.getRelativeSize(14),
                            labelrotation=15, labelcolor="g")
            plt.tick_params(axis="x", labelsize=17, labelrotation=0, labelcolor="g",
                            bottom=True, top=True, labeltop=True, labelbottom=True)
            plt.xlim(right=(1.2 * self.MaxPopulationPerCountry))  # Set Length for X-Axis
            plt.xlabel('\nPopulation in Billions', fontsize=20, color="g")  # Label for X-Axis
            plt.ylabel('')  # Label for Y-Axis

            for t in range(self.numberOfCountries):                         # Each loop for a country
                value = f'{int(topPopulationThisYearList[t]):,}'
                plt.text(topPopulationThisYearList[t] + 50000000, t,  # gap between Bars
                         value,
                         color='deepskyblue', va="center", fontsize=self.getRelativeSize(17))
                # Add rank to the graph
                plt.text(1000000, t,
                         str(t + 1),
                         color='lime', va="center", fontsize=self.getRelativeSize(17))

            # Add World Population
            plt.text(610000000, self.numberOfCountries/3,
                     'TOTAL POPULATION OF THE WORLD',
                     color='orangered', va="center", fontsize=25)

            # Insert world's population in the center
            world_population = thisYearObject.getWorldPopulationThisYear()
            world_population = self.getFormattedStr(world_population)
            plt.text(560000000, self.numberOfCountries/2,
                     world_population,
                     color='orangered', va="center", fontsize=80)

            # Signature
            plt.text(1000000000, self.numberOfCountries * 0.9,
                     'Võ Văn Thương - TP Hồ Chí Minh, Việt Nam, 09.2019'
                     '\nQuoc Huy Nguyen - Hamburg, Germany, 10.2019'
                     '\nData sources: https://data.worldbank.org',
                     color='royalblue', va="center", fontsize=13)

            self.saveImages(thisYearInt)

    def saveImages(self, thisYear):
        # Lưu biểu đồ
        filename = 'population_' + str(thisYear) + '.png'
        plt.savefig('/Users/quochuy/Desktop/Github/Population-Census/Images/' + filename, dpi=100)
        plt.gca()
        plt.close()

    def getFormattedStr(self, population):
        '''
        Conver Int to a String in form: 1.000.000
        :param population: In Type Int
        :return: String in form 1.000.000
        '''
        return f'{int(population):,}'

    def showLoading(self, process, x):
        if process == 0 and x > self.NumberOfYears / 100 * 20:
            print("Rendering 20% done")
            return 20
        if process == 20 and x > self.NumberOfYears / 100 * 40:
            print("Rendering 40% done")
            return 40
        if process == 40 and x > self.NumberOfYears / 100 * 60:
            print("Rendering 60% done")
            return 60
        if process == 60 and x > self.NumberOfYears / 100 * 80:
            print("Rendering 80% done")
            return 80
        if process == 80 and x == self.NumberOfYears - 1:
            print("Rendering 100% done")
            return 100
        else:
            return process

    def getRelativeSize(self, size):
        '''
        Convert values of sizes, so the components could stay at their positions even when the size of Images was changed
        :param size: absolute size
        :return: relative size
        '''
        return size*20/self.numberOfCountries