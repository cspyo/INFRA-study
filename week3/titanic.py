class TitanicPassenger:
    def __init__(self, PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked):
        self.id = int(PassengerId)
        self.survived = Survived
        self.p_class = Pclass
        self.name = Name
        self.sex = Sex
        self.age = int(Age) if Age != '' else None
        self.sibsp = SibSp
        self.parch = Parch
        self.ticket = Ticket
        self.fare = Fare
        self.cabin = Cabin
        self.embarked = Embarked

    def __str__(self):
        return f"Passenger ID: {self.id}, Survived: {self.survived}, Class: {self.p_class}, Name: {self.name}, Sex: {self.sex}, Age: {self.age}, SibSp: {self.sibsp}, Parch: {self.parch}, Ticket: {self.ticket}, Fare: {self.fare}, Cabin: {self.cabin}, Embarked: {self.embarked}"

    def to_tuple(self):
        return (self.id, self.survived, self.p_class, self.name, self.sex, self.age, self.sibsp, self.parch, self.ticket, self.fare, self.cabin, self.embarked)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'survived': self.survived,
            'p_class': self.p_class,
            'sex': self.sex,
            'age': self.age,
            'sibsp': self.sibsp,
            'parch': self.parch,
            'ticket': self.ticket,
            'fare': self.fare,
            'cabin': self.cabin,
            'embarked': self.embarked
        }