export interface Params {
    page?: number;
    page_size?: number;
}

export interface Pagination {
    total: number;
    total_pages: number;
    first_page: number;
    last_page: number;
    page: number;
    next_page: number;
}
