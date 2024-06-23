class MarketsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.model.set_controller(self)
        self.page_size = 30
        self.page_number = 0  # Сохраняет текущую страницу

    def run(self):
        self.model.load_data()
        self.update_table()
        self.view.show()

    def update_table(self, page_number=None):
        if page_number is not None:
            self.page_number = page_number
        data_frame = self.model.get_page(self.page_number, self.page_size)
        self.view.update_table(data_frame)

    def update_view(self):
        data_frame = self.model.get_page(self.page_number, self.page_size)
        self.view.update_table(data_frame)

    def search_markets(self, city=None, state=None, zip_code=None):
        self.view.page_number = 0  # сброс страницы к 0 перед началом нового поиска
        self.model.search_markets(city, state, zip_code)
        self.update_table()

    def get_total_pages(self, page_size):
        return self.model.get_total_pages(page_size)

    def get_market_details(self, market_name):
        return self.model.get_market_details(market_name)

    def submit_review(self, first_name, last_name, rating, review_text):
        user_id = self.model.get_user_id(first_name, last_name)
        if not user_id:
            user_id = self.model.insert_user(first_name, last_name)
        market_name = self.view.get_selected_market_name()
        market_id = self.model.get_market_id(market_name)
        if market_id:
            self.model.insert_review(market_id, user_id, rating, review_text)
            self.update_table()
