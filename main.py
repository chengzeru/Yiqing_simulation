import pygame
import random
import sys
import time
import math
from pygame.locals import *

bgColor = pygame.Color(150, 150, 150)
edgeColor = pygame.Color(0, 0, 255)
healthyState = pygame.Color(0, 255, 0)
infectState = pygame.Color(255, 255, 0)
attackState = pygame.Color(255, 0, 0)
hospitalState = pygame.Color(128, 0, 0)
deathState = pygame.Color(0, 0, 0)
recoverState = pygame.Color(255, 255, 255)

infectDays = random.randint(3, 14)
attackDays = random.randint(1, 3)
hospitalDays = random.randint(5, 8)

healthID = []
infectID = []
attackID = []
hospitalID = []

windowSize = 600
citySize = 400
peopleTotal = 1000
bedTotal = 100
infectInit = 5
moveDistancePerDay = 10.0
mask = 1
safeDistance = 3.5 * 3.5 if mask else 9 * 9
deathRate = 0.8


class typeText:
    def displayText1(self, playSurface, day):
        screenDisplayFont = pygame.font.SysFont("", 30)
        screenDisplay1 = screenDisplayFont.render("Days:" + str(day), True, recoverState)
        screenRect1 = screenDisplay1.get_rect()
        screenRect1.midtop = (50, 10)

        screenDisplay2 = screenDisplayFont.render("People:" + str(peopleTotal), True, recoverState)
        screenRect2 = screenDisplay2.get_rect()
        screenRect2.midtop = (180, 10)

        playSurface.blit(screenDisplay1, screenRect1)
        playSurface.blit(screenDisplay2, screenRect2)
        pygame.display.flip()

    def displayText2(self, playSurface, healthyNumber, infectNumber, attackNumber):
        screenDisplayFont = pygame.font.SysFont("", 30)
        screenDisplay1 = screenDisplayFont.render("Healthy:" + str(healthyNumber), True, healthyState)
        screenRect1 = screenDisplay1.get_rect()
        screenRect1.midtop = (60, 30)

        screenDisplay2 = screenDisplayFont.render("Infect:" + str(infectNumber), True, infectState)
        screenRect2 = screenDisplay2.get_rect()
        screenRect2.midtop = (200, 30)

        screenDisplay3 = screenDisplayFont.render("Attack:" + str(attackNumber), True, attackState)
        screenRect3 = screenDisplay3.get_rect()
        screenRect3.midtop = (320, 30)

        playSurface.blit(screenDisplay1, screenRect1)
        playSurface.blit(screenDisplay2, screenRect2)
        playSurface.blit(screenDisplay3, screenRect3)
        pygame.display.flip()

    def displayText3(self, playSurface, hospitalNumber, deathNumber, recoverNumber):
        screenDisplayFont = pygame.font.SysFont("", 30)
        screenDisplay1 = screenDisplayFont.render("Hospital:" + str(hospitalNumber), True, hospitalState)
        screenRect1 = screenDisplay1.get_rect()
        screenRect1.midtop = (60, 60)

        screenDisplay2 = screenDisplayFont.render("Death:" + str(deathNumber), True, deathState)
        screenRect2 = screenDisplay2.get_rect()
        screenRect2.midtop = (200, 60)

        screenDisplay3 = screenDisplayFont.render("Recover:" + str(recoverNumber), True, recoverState)
        screenRect3 = screenDisplay3.get_rect()
        screenRect3.midtop = (320, 60)

        playSurface.blit(screenDisplay1, screenRect1)
        playSurface.blit(screenDisplay2, screenRect2)
        playSurface.blit(screenDisplay3, screenRect3)
        pygame.display.flip()

    def displayText4(self, playSurface):
        screenDisplayFont = pygame.font.SysFont("", 30)
        screenDisplay1 = screenDisplayFont.render("City:", True, recoverState)
        screenRect1 = screenDisplay1.get_rect()
        screenRect1.midtop = (220, 120)

        screenDisplay2 = screenDisplayFont.render("Hospital:", True, recoverState)
        screenRect2 = screenDisplay2.get_rect()
        screenRect2.midtop = (500, 20)

        playSurface.blit(screenDisplay1, screenRect1)
        playSurface.blit(screenDisplay2, screenRect2)
        pygame.display.flip()

    def gameOver1(self, playSurface):
        gameOverFont = pygame.font.SysFont("", 128)
        gameOverSurf = gameOverFont.render("Fail", True, recoverState)
        gameOverRect = gameOverSurf.get_rect()
        gameOverRect.midtop = (320, 300)
        playSurface.blit(gameOverSurf, gameOverRect)
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    def gameOver2(self, playSurface):
        gameOverFont = pygame.font.SysFont("", 128)
        gameOverSurf = gameOverFont.render("Success", True, recoverState)
        gameOverRect = gameOverSurf.get_rect()
        gameOverRect.midtop = (320, 300)
        playSurface.blit(gameOverSurf, gameOverRect)
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()


class typeHospital:
    def __init__(self):
        self.hospitalX = 460
        self.hospitalY = 50
        self.hospitalWidth = 80
        self.hospitalHeight = 500
        self.beds = bedTotal
        self.bedSize = 10
        self.dx = 0
        self.dy = 0
        self.step = 0

    def bedJudge(self):
        return self.beds > len(hospitalID)

    def draw(self, playSurface):
        pygame.draw.rect(playSurface, edgeColor,
                         [self.hospitalX, self.hospitalY, self.hospitalWidth, self.hospitalHeight], 1)

        for i in range(self.beds):
            self.dx = self.hospitalX + (i % 4) * 20 + 5
            self.dy = self.hospitalY + (i // 4) * 20 + 5
            pygame.draw.rect(playSurface, edgeColor, [self.dx, self.dy, self.bedSize, self.bedSize], 0)

        self.step = 0
        for p in peopleGroup:
            if p.state == hospitalState:
                self.dx = self.hospitalX + (self.step % 4) * 20 + 5
                self.dy = self.hospitalY + (self.step // 4) * 20 + 5
                pygame.draw.rect(playSurface, hospitalState, [self.dx, self.dy, self.bedSize, self.bedSize], 0)
                self.step += 1

        pygame.display.flip()


class typePeople:
    def __init__(self):
        self.state = healthyState
        self.days = 0
        self.peopleSize = 4
        self.theta = round(random.uniform(0, 6.28), 2)
        self.r = random.randrange(0, 180)
        self.positionX = math.cos(self.theta) * self.r
        self.positionY = math.sin(self.theta) * self.r
        self.direction = round(random.uniform(0, 6.28), 2)
        self.dx = 0
        self.dy = 0
        self.newPositionX = 0
        self.newPositionY = 0
        self.distance = 0

    def move(self, days):
        if self.state == hospitalState or self.state == deathState:
            return
        self.dx = moveDistancePerDay * math.cos(self.direction)
        self.dy = moveDistancePerDay * math.sin(self.direction)
        self.newPositionX = self.positionX + self.dx
        self.newPositionY = self.positionY + self.dy
        self.distance = self.newPositionX ** 2 + self.newPositionY ** 2
        if self.distance < (citySize / 2 - 10) ** 2:
            self.positionX = self.newPositionX
            self.positionY = self.newPositionY
        else:
            self.direction = round(random.uniform(0, 6.28), 2)
            self.move(days)


class typeCity:
    def __init__(self):
        self.tempID = []
        self.twoPeopleDistance = 0
        self.cityX = 220
        self.cityY = 350
        self.citySize = citySize

        self.healthyNumber = 0
        self.infectNumber = 0
        self.attackNumber = 0
        self.hospitalNumber = 0
        self.deathNumber = 0
        self.recoverNumber = 0

        for a in range(peopleTotal):
            healthID.append(a)
        for a in range(infectInit):
            x = random.randint(0, peopleTotal - 1)
            if peopleGroup[x].state == healthyState:
                peopleGroup[x].state = infectState
                peopleGroup[x].days = infectDays
                healthID.remove(x)
                infectID.append(x)

    def simulatesOneDay(self):
        self.tempID = []
        for i in healthID:
            for j in infectID:
                self.twoPeopleDistance = (peopleGroup[i].positionX - peopleGroup[j].positionX) ** 2 \
                                         + (peopleGroup[i].positionY - peopleGroup[j].positionY) ** 2
                if self.twoPeopleDistance < safeDistance:
                    self.tempID.append(i)
                    break
        for i in self.tempID:
            peopleGroup[i].state = infectState
            peopleGroup[i].days = infectDays
            healthID.remove(i)
            infectID.append(i)
        for i in range(peopleTotal):
            if peopleGroup[i].state == infectState:
                peopleGroup[i].days -= 1
                if peopleGroup[i].days <= 0:
                    peopleGroup[i].state = attackState
                    peopleGroup[i].days = attackDays
                    infectID.remove(i)
                    attackID.append(i)
                continue

            if peopleGroup[i].state == attackState:
                peopleGroup[i].days -= 1
                if peopleGroup[i].days <= 0:
                    if hospital.bedJudge():
                        attackID.remove(i)
                        hospitalID.append(i)
                        peopleGroup[i].state = hospitalState
                        peopleGroup[i].days = hospitalDays
                    elif round(random.uniform(0, 1), 2) < deathRate:
                        attackID.remove(i)
                        peopleGroup[i].state = deathState
                    else:
                        attackID.remove(i)
                        peopleGroup[i].state = recoverState

            if peopleGroup[i].state == hospitalState:
                peopleGroup[i].days -= 1
                if peopleGroup[i].days <= 0:
                    peopleGroup[i].state = recoverState
                    hospitalID.remove(i)
                    continue

    def draw(self, playSurface):
        pygame.draw.circle(playSurface, edgeColor, (self.cityX, self.cityY), self.citySize / 2, 1)
        pygame.display.flip()

    def countPeople(self):
        self.healthyNumber = 0
        self.infectNumber = 0
        self.attackNumber = 0
        self.hospitalNumber = 0
        self.deathNumber = 0
        self.recoverNumber = 0
        for i in range(peopleTotal):
            if peopleGroup[i].state == healthyState:
                self.healthyNumber += 1
            if peopleGroup[i].state == infectState:
                self.infectNumber += 1
            if peopleGroup[i].state == attackState:
                self.attackNumber += 1
            if peopleGroup[i].state == hospitalState:
                self.hospitalNumber += 1
            if peopleGroup[i].state == deathState:
                self.deathNumber += 1
            if peopleGroup[i].state == recoverState:
                self.recoverNumber += 1


text = typeText()

peopleGroup = []
for i in range(peopleTotal):
    people = typePeople()
    peopleGroup.append(people)

hospital = typeHospital()

city = typeCity()


def main():
    pygame.init()
    playSurface = pygame.display.set_mode((windowSize, windowSize))
    pygame.display.set_caption("病毒传播仿真程序")
    totalDays = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        playSurface.fill(bgColor)
        pygame.time.Clock().tick(20)
        totalDays += 1
        city.countPeople()
        text.displayText1(playSurface, totalDays)
        text.displayText2(playSurface, city.healthyNumber, city.infectNumber, city.attackNumber)
        text.displayText3(playSurface, city.hospitalNumber, city.deathNumber, city.recoverNumber)
        text.displayText4(playSurface)
        city.draw(playSurface)
        hospital.draw(playSurface)
        for p in peopleGroup:
            if p.state != hospitalState:
                pygame.draw.rect(playSurface, p.state,
                                 [220 + p.positionX, 350 + p.positionY, p.peopleSize, p.peopleSize], 0)
        for p in peopleGroup:
            p.move(totalDays)
        city.simulatesOneDay()
        if city.infectNumber == 0 and city.deathNumber > peopleTotal / 2:
            text.gameOver1(playSurface)
        elif city.infectNumber == 0 and city.deathNumber <= peopleTotal / 2 and city.attackNumber == 0:
            text.gameOver2(playSurface)
        pygame.display.flip()


if __name__ == "__main__":
    main()
