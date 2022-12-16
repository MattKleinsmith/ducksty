import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getReviewsByProductId } from "../../../../store/productReviews";
import FiveStars from "../../../FiveStars/FiveStars";
import ProductDetailsReview from "./ProductDetailsReview/ProductDetailsReview";
import styles from "./ProductDetailsReviewList.module.css";

export default function ProductDetailsReviewList({ product }) {
    const dispatch = useDispatch();
    const reviews = useSelector(state => Object.values(state.productReviews));
    useEffect(() => {
        dispatch(getReviewsByProductId(product.id));
    }, [dispatch, product.id]);

    if (!reviews) return;
    return (
        <div className={styles.ProductDetailsReviewListWrapper}>
            <div className={styles.reviewSummary}>
                {reviews.length} reviews {(Math.round(product.seller_rating * 100) / 100).toFixed(2)} <FiveStars rating={product.seller_rating} />
            </div>
            <div className={styles.ProductDetailsReviewList}>
                {reviews.map((review, i) => <ProductDetailsReview key={i} review={review} />)}
            </div>
        </div>
    );
}
